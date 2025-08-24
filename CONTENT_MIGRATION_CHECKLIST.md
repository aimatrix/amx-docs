# AIMatrix Documentation Migration Checklist

**Migration Overview**: Restructuring from current 210 files (107 business, 101 technical, 2 blogs) to new 6-section structure with consolidated content and flatter hierarchy.

**Current Structure Issues**:
- 35 empty directories to clean up
- Significant duplication between business/technical sections
- Deep hierarchy (4+ levels in many areas)
- Content scattered across multiple similar sections

**Target Structure**: 6 main sections with max 3 levels depth:
- `get-started/` - Onboarding and quickstart content
- `products/` - Product documentation and features
- `build/` - Technical implementation and development
- `solutions/` - Industry solutions and use cases
- `reference/` - API, SDK, and technical reference
- `resources/` - Community, support, and additional resources

---

## 🚨 PRE-MIGRATION TASKS

### 1. Backup and Safety Measures
**Priority**: Critical | **Effort**: Quick | **Dependencies**: None | **Risk**: High if skipped

- [ ] **Create full backup branch**
  ```bash
  git checkout -b backup/pre-migration-$(date +%Y%m%d)
  git push origin backup/pre-migration-$(date +%Y%m%d)
  ```
- [ ] **Export current site build**
  ```bash
  hugo --destination backup/current-site-build
  ```
- [ ] **Document all current URLs** for redirect mapping
  ```bash
  find content/en -name "*.md" | sed 's|content/en/||' | sed 's|/_index.md|/|' | sed 's|\.md|/|' > migration-urls.txt
  ```
- [ ] **Create migration working branch**
  ```bash
  git checkout -b feature/content-restructure
  ```

### 2. Content Audit and Analysis
**Priority**: Critical | **Effort**: Moderate | **Dependencies**: Backup complete | **Risk**: Medium

- [ ] **Generate content inventory report**
  ```bash
  find content/en -name "*.md" -exec wc -l {} + | sort -n > content-sizes.txt
  ```
- [ ] **Identify duplicate content patterns**
  - [ ] Compare business/products/ vs technical/products/
  - [ ] Compare business/services/ vs technical/services/
  - [ ] Map duplicate use-case content
  - [ ] List identical or near-identical files
- [ ] **Map empty directories for cleanup**
  ```bash
  find content/en -type d -empty > empty-dirs.txt
  ```
- [ ] **Analyze internal link dependencies**
- [ ] **Identify orphaned content** (no incoming links)
- [ ] **Create content consolidation plan** with merge decisions

### 3. Migration Environment Setup
**Priority**: High | **Effort**: Quick | **Dependencies**: None | **Risk**: Low

- [ ] **Test Hugo build in clean environment**
- [ ] **Verify all dependencies** (themes, assets, etc.)
- [ ] **Set up staging deployment** for testing
- [ ] **Create migration scripts directory**
  ```bash
  mkdir -p scripts/migration
  ```
- [ ] **Prepare redirect configuration files**

---

## 🔄 CONTENT CONSOLIDATION TASKS

### 4. Identify and Merge Duplicate Content
**Priority**: Critical | **Effort**: Complex | **Dependencies**: Audit complete | **Risk**: High - content loss

#### 4.1 Products Section Consolidation
- [ ] **Merge business/products/ with technical/products/**
  - [ ] AIMatrix CLI: Merge `business/products/aimatrix-cli.md` + `technical/products/aimatrix-cli-technical.md`
  - [ ] AMX Console: Merge business + technical versions
  - [ ] AMX Engine: Consolidate architecture + business info
  - [ ] AMX Hub: Combine feature + technical specs
- [ ] **Decision**: Keep comprehensive version, archive duplicates
- [ ] **Cross-reference**: Ensure no broken internal links

#### 4.2 Services Section Consolidation
- [ ] **Business Services + Technical Services merge**
  - [ ] Agent Design Service (2 versions exist)
  - [ ] AI Model Training (2 versions exist)  
  - [ ] Content Publishing (2 versions exist)
  - [ ] Data Hub Integration (2 versions exist)
  - [ ] Knowledge Pipeline (2 versions exist)
  - [ ] Video Intelligence (2 versions exist)
- [ ] **Create unified service pages** with both business value + technical implementation

#### 4.3 Use Cases Consolidation
- [ ] **Audit business/use-cases/ structure**
  - [ ] Customer Service AI (8 sub-pages)
  - [ ] Digital Marketing AI (10 sub-pages)
  - [ ] Financial Control AI (10 sub-pages)
  - [ ] Learning Management AI (10 sub-pages)
  - [ ] Sales Funnel AI (10 sub-pages)
  - [ ] SysOps DevOps AI (10 sub-pages)
- [ ] **Consolidate with solutions/ approach** - group by industry vs function
- [ ] **Remove empty use-case directories**: hr-admin-ai/, finance-compliance-ai/

#### 4.4 Architecture & Technical Docs
- [ ] **Merge overlapping architecture content**
  - [ ] business/integration-architecture.md
  - [ ] technical/architecture/ (multiple files)
  - [ ] technical/intelligent-systems/ content
- [ ] **Consolidate getting started content**
  - [ ] Various quickstart scattered across sections
  - [ ] Developer onboarding in multiple places

### 5. Content Quality Review
**Priority**: High | **Effort**: Moderate | **Dependencies**: Consolidation | **Risk**: Medium

- [ ] **Review merged content for:**
  - [ ] Duplicate headings and sections
  - [ ] Conflicting information
  - [ ] Outdated technical details
  - [ ] Broken internal links
  - [ ] Missing front matter consistency
- [ ] **Standardize front matter** across all files
- [ ] **Fix duplicate H1 headers** (as per CLAUDE.md instructions)
- [ ] **Update navigation weights** and hierarchy

---

## 📁 FILE MIGRATION TASKS

### 6. Create New Directory Structure
**Priority**: High | **Effort**: Quick | **Dependencies**: Planning complete | **Risk**: Low

```bash
# Create new structure
mkdir -p content/en/{get-started,products,build,solutions,reference,resources}
mkdir -p content/en/get-started/{quickstart,installation,tutorials}
mkdir -p content/en/products/{aimatrix-cli,amx-console,amx-engine,amx-hub}
mkdir -p content/en/build/{development,integration,deployment,architecture}
mkdir -p content/en/solutions/{retail,manufacturing,finance,healthcare}
mkdir -p content/en/reference/{api,sdk,glossary}
mkdir -p content/en/resources/{community,support,downloads}
```

### 7. Migrate Core Content Sections

#### 7.1 GET-STARTED Section Migration
**Priority**: Critical | **Effort**: Moderate | **Dependencies**: Structure created | **Risk**: Medium

- [ ] **Move quickstart content**
  - Source: `technical/supabase-platform/quick-start.md`
  - Destination: `get-started/quickstart.md`
- [ ] **Create installation guide**
  - Consolidate from various setup instructions
  - Include CLI installation, Docker setup, etc.
- [ ] **Migrate basic tutorials**
  - Source: `technical/tutorials/` content
  - Filter and consolidate beginner content
- [ ] **Create architecture overview**
  - Source: Various architecture docs
  - Create single high-level overview

#### 7.2 PRODUCTS Section Migration  
**Priority**: Critical | **Effort**: Complex | **Dependencies**: Consolidation complete | **Risk**: High

- [ ] **AIMatrix CLI**
  - Merge: `business/products/aimatrix-cli.md` + `technical/products/aimatrix-cli-technical.md`
  - Destination: `products/aimatrix-cli/_index.md`
- [ ] **AMX Console**
  - Merge: Business + technical console docs
  - Destination: `products/amx-console/_index.md`
- [ ] **AMX Engine**
  - Merge: Engine business + technical architecture
  - Destination: `products/amx-engine/_index.md`
- [ ] **AMX Hub** 
  - Consolidate hub documentation
  - Destination: `products/amx-hub/_index.md`

#### 7.3 BUILD Section Migration
**Priority**: High | **Effort**: Complex | **Dependencies**: Architecture docs ready | **Risk**: High

- [ ] **Development Guides**
  - Source: `technical/developers/`, `technical/developer/`
  - Consolidate developer resources
  - Destination: `build/development/`
- [ ] **Integration Guides**
  - Source: `technical/integration/`, `business/integration-architecture.md`
  - Destination: `build/integration/`
- [ ] **Deployment Documentation**
  - Source: `technical/applications/deployment-strategies.md`
  - Add cloud, edge, on-premise guides
  - Destination: `build/deployment/`
- [ ] **Architecture Specifications**
  - Source: `technical/architecture/`, `technical/specs/`
  - Consolidate technical architecture
  - Destination: `build/architecture/`

#### 7.4 SOLUTIONS Section Migration
**Priority**: High | **Effort**: Complex | **Dependencies**: Use-case consolidation | **Risk**: Medium

- [ ] **Retail Solutions**
  - Source: `business/use-cases/retail-ai/`
  - Destination: `solutions/retail/`
- [ ] **Manufacturing Solutions**
  - Source: Various manufacturing content
  - Destination: `solutions/manufacturing/`
- [ ] **Finance Solutions** 
  - Source: `business/use-cases/financial-control-ai/`
  - Destination: `solutions/finance/`
- [ ] **Healthcare Solutions**
  - Source: Scattered healthcare content
  - Destination: `solutions/healthcare/`

#### 7.5 REFERENCE Section Migration
**Priority**: High | **Effort**: Moderate | **Dependencies**: Technical docs ready | **Risk**: Medium

- [ ] **API Reference**
  - Source: `technical/apis/`
  - Consolidate REST, GraphQL, WebSocket docs
  - Destination: `reference/api/`
- [ ] **SDK Documentation**
  - Source: `technical/sdks/`
  - Destination: `reference/sdk/`
- [ ] **Technical Glossary**
  - Create from scattered terminology
  - Source: `business/key-concepts/`
  - Destination: `reference/glossary/`

#### 7.6 RESOURCES Section Migration
**Priority**: Medium | **Effort**: Moderate | **Dependencies**: Community content | **Risk**: Low

- [ ] **Community Resources**
  - Source: Various community references
  - Destination: `resources/community/`
- [ ] **Support Documentation**
  - Source: Support and troubleshooting content
  - Destination: `resources/support/`
- [ ] **Downloads**
  - Source: `technical/downloads/`
  - Destination: `resources/downloads/`

---

## 🧹 POST-MIGRATION CLEANUP

### 8. Remove Old Structure
**Priority**: High | **Effort**: Quick | **Dependencies**: Migration complete | **Risk**: High if done too early

⚠️ **DANGER ZONE** - Only execute after confirming successful migration

- [ ] **Remove empty directories**
  ```bash
  find content/en -type d -empty -delete
  ```
- [ ] **Archive old business/ directory**
  ```bash
  git mv content/en/business content/en/_archived/business-old
  ```
- [ ] **Archive old technical/ directory**
  ```bash
  git mv content/en/technical content/en/_archived/technical-old
  ```
- [ ] **Clean up orphaned assets**
- [ ] **Remove duplicate image files**

### 9. Navigation and Menu Updates
**Priority**: Critical | **Effort**: Moderate | **Dependencies**: Structure finalized | **Risk**: Medium

- [ ] **Update hugo.yaml navigation**
  - Remove old business/technical menus
  - Add new 6-section menu structure
- [ ] **Update sidebar navigation** in theme
- [ ] **Configure menu weights** for proper ordering
- [ ] **Test navigation on all devices**
- [ ] **Update breadcrumb configuration**

### 10. URL Redirects and SEO
**Priority**: Critical | **Effort**: Complex | **Dependencies**: URL mapping complete | **Risk**: High SEO impact

- [ ] **Create redirect rules file**
  ```bash
  # CloudFront redirects or .htaccess
  /business/products/aimatrix-cli/ -> /products/aimatrix-cli/
  /technical/developers/ -> /build/development/
  ```
- [ ] **Update internal links** throughout content
- [ ] **Generate sitemap** with new structure
- [ ] **Update robots.txt** if needed
- [ ] **Configure analytics** for new URL structure

---

## ✅ QUALITY ASSURANCE CHECKS

### 11. Technical Validation
**Priority**: Critical | **Effort**: Moderate | **Dependencies**: Migration complete | **Risk**: High

- [ ] **Hugo build validation**
  ```bash
  hugo --gc --minify --enableGitInfo
  ```
- [ ] **Check for build warnings/errors**
- [ ] **Validate all internal links**
  ```bash
  hugo server --navigateToChanged --templateMetrics --path-warnings
  ```
- [ ] **Test site search functionality**
- [ ] **Verify RSS feeds** still work
- [ ] **Check image loading** and assets

### 12. Content Quality Checks
**Priority**: High | **Effort**: Moderate | **Dependencies**: Technical validation | **Risk**: Medium

- [ ] **No duplicate H1 headers** (per CLAUDE.md rules)
- [ ] **Consistent front matter** across all files
- [ ] **Working cross-references** between sections
- [ ] **Proper image alt tags** and accessibility
- [ ] **Spell check** and grammar review
- [ ] **Technical accuracy** review by SME

### 13. User Experience Testing
**Priority**: High | **Effort**: Moderate | **Dependencies**: Content quality complete | **Risk**: Medium

- [ ] **Navigation flow testing**
  - Can users find information quickly?
  - Is the hierarchy logical?
  - Are there too many clicks to reach content?
- [ ] **Search functionality testing**
- [ ] **Mobile responsive testing**
- [ ] **Page load speed testing**
- [ ] **Cross-browser compatibility**

### 14. SEO and Analytics Validation
**Priority**: High | **Effort**: Quick | **Dependencies**: Site deployed | **Risk**: Medium

- [ ] **Google Search Console** - submit new sitemap
- [ ] **Analytics tracking** - verify events fire correctly
- [ ] **Meta descriptions** and titles are appropriate
- [ ] **Schema markup** validation
- [ ] **Social sharing** previews work correctly

---

## 🚀 DEPLOYMENT AND ROLLOUT

### 15. Staged Deployment
**Priority**: Critical | **Effort**: Quick | **Dependencies**: QA complete | **Risk**: High

- [ ] **Deploy to staging environment**
  ```bash
  # Deploy branch to staging
  git push origin feature/content-restructure:staging
  ```
- [ ] **Stakeholder review** and approval
- [ ] **Final content review** on staging
- [ ] **Performance testing** on staging
- [ ] **Load testing** if expecting traffic spike

### 16. Production Deployment
**Priority**: Critical | **Effort**: Quick | **Dependencies**: Staging approved | **Risk**: Very High

- [ ] **Schedule deployment window** (low traffic time)
- [ ] **Merge to main branch**
  ```bash
  git checkout main
  git merge feature/content-restructure
  ```
- [ ] **Deploy via GitHub Actions**
- [ ] **Monitor deployment logs**
- [ ] **Verify CloudFront invalidation**
- [ ] **Test critical user journeys**

### 17. Post-Deployment Monitoring
**Priority**: Critical | **Effort**: Ongoing | **Dependencies**: Deployment complete | **Risk**: Medium

- [ ] **Monitor 404 errors** - fix with redirects
- [ ] **Track user behavior** changes in analytics
- [ ] **Monitor search rankings** for key terms
- [ ] **Collect user feedback** on new structure
- [ ] **Performance monitoring** for site speed
- [ ] **Watch for broken links** reports

---

## 📊 SUCCESS METRICS & VALIDATION

### Success Criteria:
- [ ] **Zero broken internal links**
- [ ] **All content migrated** (no orphaned files)
- [ ] **Hugo builds without errors**
- [ ] **Site search returns relevant results**
- [ ] **Page load times <3 seconds**
- [ ] **Mobile responsive score >95%**
- [ ] **SEO audit score maintained/improved**

### Content Metrics:
- [ ] **File count reduced** from 210 to target range (150-180)
- [ ] **Directory depth reduced** to max 3 levels
- [ ] **Duplicate content eliminated** (>90% reduction)
- [ ] **Empty directories removed** (all 35)

### User Experience Metrics:
- [ ] **Navigation clicks to content** reduced by 25%
- [ ] **Search success rate** >80%
- [ ] **Bounce rate maintained** or improved
- [ ] **User feedback** positive on new structure

---

## ⚠️ RISKS AND MITIGATION

### High-Risk Areas:
1. **SEO Impact** - Mitigation: Comprehensive redirects, gradual rollout
2. **Content Loss** - Mitigation: Full backups, careful review process  
3. **Broken Links** - Mitigation: Link validation tools, thorough testing
4. **User Confusion** - Mitigation: Communication plan, gradual rollout

### Rollback Plan:
- [ ] Keep backup branch available for 30 days
- [ ] Document exact steps to revert
- [ ] Test rollback procedure on staging
- [ ] Have emergency contact list ready

---

**Migration Owner**: Content Team  
**Technical Lead**: Development Team  
**Approval Required**: Vincent (Product Owner)  
**Timeline Estimate**: 2-3 weeks full-time effort  
**Go/No-Go Decision Point**: After QA validation complete

*This checklist should be executed in order, with each phase building on the previous. Do not skip pre-migration tasks or proceed to later phases without completing dependencies.*