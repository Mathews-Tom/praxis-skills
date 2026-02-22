# GraphQL Queries Reference

## Cost Model

GitHub's GraphQL API enforces a point budget of **5000 points per hour** for authenticated
users. Query cost depends on the number of nodes requested.

**Cost formula:**

```
cost = nodes_requested × (1 + child_nodes_requested)
```

A query requesting 100 issues, each with 10 labels, costs `100 × (1 + 10) = 1100` points.

### Introspect Current Rate Limit

```bash
gh api graphql -f query='
  query {
    rateLimit {
      limit
      cost
      remaining
      resetAt
      nodeCount
    }
  }
' --jq '.data.rateLimit'
```

The `cost` field in the response shows the actual cost of the query. Use this to calibrate
page sizes before running bulk operations.

---

## Bulk PR Status Query

Fetch open PRs with review decision and CI rollup in a single query:

```bash
gh api graphql -f query='
  query {
    repository(owner: "owner", name: "repo") {
      pullRequests(first: 20, states: OPEN) {
        nodes {
          number
          title
          reviewDecision
          commits(last: 1) {
            nodes {
              commit {
                statusCheckRollup {
                  state
                }
              }
            }
          }
        }
      }
    }
  }
' --jq '.data.repository.pullRequests.nodes[] |
  "\(.number) \(.reviewDecision // "PENDING") CI:\(.commits.nodes[0].commit.statusCheckRollup.state // "NONE") \(.title)"'
```

**Review decision states:** `APPROVED`, `CHANGES_REQUESTED`, `REVIEW_REQUIRED`, or null
(no reviewers assigned).

**CI rollup states:** `SUCCESS`, `FAILURE`, `PENDING`, `ERROR`, or null (no checks configured).

---

## Org and Team Membership

Single query replacing multiple REST calls (`/orgs/members` + `/teams` + `/teams/members`):

```bash
gh api graphql -f query='
  query {
    organization(login: "some-org") {
      teams(first: 10) {
        nodes {
          name
          slug
          members(first: 50) {
            nodes {
              login
              name
            }
          }
        }
      }
    }
  }
' --jq '.data.organization.teams.nodes[] |
  "\(.name) (\(.slug)): \(.members.nodes | map(.login) | join(", "))"'
```

This eliminates the N+1 problem of fetching each team's members individually via REST.

---

## ProjectV2 Queries

ProjectV2 boards are only accessible via GraphQL. There is no REST equivalent.

List project items with status field values:

```bash
gh api graphql -f query='
  query {
    node(id: "PVT_kwHOABCDEF") {
      ... on ProjectV2 {
        title
        items(first: 30) {
          nodes {
            content {
              ... on Issue { number title }
              ... on PullRequest { number title }
            }
            fieldValueByName(name: "Status") {
              ... on ProjectV2ItemFieldSingleSelectValue { name }
            }
          }
        }
      }
    }
  }
' --jq '.data.node.items.nodes[] |
  "\(.fieldValueByName.name // "No Status") #\(.content.number) \(.content.title)"'
```

Find the project node ID using:

```bash
gh api graphql -f query='
  query {
    organization(login: "some-org") {
      projectsV2(first: 10) {
        nodes { id title }
      }
    }
  }
' --jq '.data.organization.projectsV2.nodes[]'
```

---

## Mutations

### Add Label to Issue

```bash
gh api graphql -f query='
  mutation {
    addLabelsToLabelable(input: {
      labelableId: "I_kwDOABCDEF"
      labelIds: ["LA_kwDOABCDEF"]
    }) {
      labelable {
        ... on Issue { number title }
      }
    }
  }
'
```

Find the issue node ID and label ID first:

```bash
gh api graphql -f query='
  query {
    repository(owner: "owner", name: "repo") {
      issue(number: 42) { id }
      label(name: "bug") { id }
    }
  }
' --jq '.data.repository'
```

### Close Issue

```bash
gh api graphql -f query='
  mutation {
    closeIssue(input: {
      issueId: "I_kwDOABCDEF"
      stateReason: COMPLETED
    }) {
      issue { number state }
    }
  }
'
```

State reason options: `COMPLETED`, `NOT_PLANNED`.

---

## Rate Limit Inspection and Backoff

### Check Remaining Budget

```bash
gh api graphql -f query='{ rateLimit { remaining resetAt } }' \
  --jq '"\(.data.rateLimit.remaining) points remaining, resets at \(.data.rateLimit.resetAt)"'
```

### Backoff Strategy

When `remaining` drops below 500 points:

1. Check `resetAt` timestamp to determine wait duration.
2. Reduce `first`/`last` page sizes from 100 to 10-20.
3. Batch related queries into a single request using aliases:

```bash
gh api graphql -f query='
  query {
    repo1: repository(owner: "owner", name: "repo1") {
      issues(first: 5, states: OPEN) { totalCount }
    }
    repo2: repository(owner: "owner", name: "repo2") {
      issues(first: 5, states: OPEN) { totalCount }
    }
    rateLimit { remaining resetAt }
  }
' --jq '{repo1: .data.repo1.issues.totalCount, repo2: .data.repo2.issues.totalCount, remaining: .data.rateLimit.remaining}'
```

4. If `remaining` reaches 0, wait until `resetAt` before sending further queries.
