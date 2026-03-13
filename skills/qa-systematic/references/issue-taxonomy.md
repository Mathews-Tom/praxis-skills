# QA Issue Taxonomy

## Severity Levels

### Critical
Issues that block core user workflows or cause data loss.
- Application crash or unrecoverable error
- Authentication/authorization failure
- Data loss or corruption
- Security vulnerability (XSS, injection, exposed credentials)
- Core feature completely non-functional

### Major
Issues that significantly degrade the user experience but have workarounds.
- Feature partially broken (works in some cases, fails in others)
- Performance degradation (>3s load time on standard connection)
- Accessibility barrier (screen reader cannot access core content)
- Misleading error messages or missing error handling
- Layout broken on common viewport sizes

### Minor
Cosmetic issues or polish items that don't affect functionality.
- Alignment inconsistencies
- Typos or grammatical errors in UI text
- Missing hover states or focus indicators
- Non-standard spacing or padding
- Console warnings (not errors)

## Categories

### Functional
Core features and business logic — does the app do what it claims?

### Visual
Layout, styling, design consistency — does it look correct?

### Accessibility
Screen reader support, keyboard navigation, color contrast, ARIA — can all users access it?

### Performance
Load times, interaction responsiveness, resource usage — is it fast enough?

### Content
Text accuracy, completeness, tone consistency — is the content correct?

### Navigation
Routing, links, breadcrumbs, back button — can users get where they need to go?

### Security
Client-side security issues — exposed data, insecure forms, mixed content

### Console
JavaScript errors, failed requests, deprecation warnings — is the runtime clean?
