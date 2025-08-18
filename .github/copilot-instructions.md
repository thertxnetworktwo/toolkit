# Toolkit Repository - GitHub Copilot Instructions

**ALWAYS follow these instructions first and only fallback to additional search and context gathering if the information in these instructions is incomplete or found to be in error.**

## Repository State
This is currently a minimal toolkit repository containing only basic documentation. The repository is in its initial state and does not yet contain:
- Source code or applications to build
- Build systems or configuration files  
- Test suites or testing infrastructure
- Package managers or dependency files
- CI/CD pipelines

## Working Effectively

### Repository Structure
- **Current state**: Repository contains only README.md with basic project title
- **Root directory**: `/home/runner/work/toolkit/toolkit` (when working in sandboxed environment)
- **Key files**: 
  - `README.md` - Basic project documentation
  - `.github/copilot-instructions.md` - These instructions

### Build and Development Commands
**IMPORTANT: No build commands are currently available** since this repository does not contain source code or build configuration.

When this repository is populated with actual toolkit components, typical commands might include:
- Language-specific build commands (e.g., `npm install && npm run build`, `make`, `cargo build`)
- Test execution (e.g., `npm test`, `make test`, `pytest`)
- Linting and formatting (e.g., `npm run lint`, `gofmt`, `rustfmt`)

### Current Validation Steps
Since there is no code to build or test:
1. **File integrity check**: `ls -la` to verify repository contents
2. **README validation**: `cat README.md` to confirm basic documentation
3. **Git status check**: `git status` to verify repository state

### Dependencies and Prerequisites  
**Current requirements**: None - repository has no dependencies
**Future requirements**: When code is added, document specific:
- Programming language versions
- Build tools and their versions
- System dependencies
- Installation commands with exact URLs and versions

## Development Guidelines

### Before Making Changes
1. **Always run**: `git status` to understand current repository state
2. **Check repository contents**: `ls -la` to see what files exist
3. **Review documentation**: `cat README.md` and any other .md files

### After Making Changes
1. **Verify additions**: `git status` and `git diff` to review changes
2. **Test additions**: When code is present, always run build and test commands
3. **Update documentation**: Ensure README.md reflects new capabilities

### Common Tasks

#### Repository Inspection
```bash
# View repository contents
ls -la

# Check git status  
git status

# View basic documentation
cat README.md

# Check repository structure
find . -type f -name "*.md" -o -name "*.json" -o -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" -o -name "*.rs" | head -20
```

#### When Source Code is Added
Update these instructions to include:
- **Exact build commands** with verified timeout values
- **Test execution steps** with timing expectations  
- **CRITICAL**: Add "NEVER CANCEL" warnings for any command taking >2 minutes
- **Dependency installation** with specific versions and URLs
- **Validation scenarios** for testing functionality
- **Linting and formatting** commands to pass CI

## Timing Expectations
**Current operations**: All current commands complete in <5 seconds
**Future builds**: When build systems are added, document actual timing:
- Build time: [TO BE MEASURED] - Set timeout to [TIME + 50%] minutes
- Test time: [TO BE MEASURED] - Set timeout to [TIME + 50%] minutes  
- **NEVER CANCEL long-running operations** - document expected duration

## Validation Scenarios
**Current**: No functional scenarios available due to lack of application code
**Future**: When applications are added, include specific user scenarios:
- End-to-end workflows to test after changes
- CLI command examples with expected outputs
- API endpoints to verify (if applicable)
- UI flows to validate (if applicable)

## Troubleshooting

### Common Issues
- **Empty repository**: This is expected - repository is in initial state
- **No build files**: Normal for current state - add build configuration as toolkit develops
- **No dependencies**: Expected - dependency files will be added with source code

### When Issues Arise
1. Check git status for repository state
2. Verify you're in correct directory: `/home/runner/work/toolkit/toolkit`
3. Review recent commits: `git log --oneline -5`
4. Check for any new files: `ls -la`

## Future Development Notes
When adding components to this toolkit repository:

1. **Update these instructions immediately** with new build/test commands
2. **Measure and document timing** for all new operations
3. **Add explicit timeout values** for any command taking >2 minutes
4. **Include "NEVER CANCEL" warnings** for long-running operations
5. **Define validation scenarios** for new functionality
6. **Document dependencies** with exact installation commands
7. **Add linting/formatting** requirements for CI compliance

## Key Information for Coding Agents
- **Repository type**: Toolkit (intended for utility/tool development)
- **Current development stage**: Initial/Bootstrap
- **Build status**: No build system present
- **Test status**: No test infrastructure present  
- **Dependencies**: None currently required
- **Platform support**: To be determined as code is added
- **Documentation**: Minimal - README.md only

Always update these instructions as the repository evolves to ensure they remain accurate and helpful for development work.