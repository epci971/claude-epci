# /wd:benchmark - Performance Testing & Optimization

## Purpose
Performance testing and optimization with visual reports and actionable insights.

## Usage
```
/wd:benchmark [target] [--metrics performance|accessibility|seo|all] [--compare <baseline>] [--export <path>]
```

## Auto-Persona Activation
- **Performance**: Optimization specialist and metrics analysis
- **QA**: Testing validation and quality assurance

## MCP Integration
- **Playwright**: Performance metrics collection and browser automation
- **Sequential**: Systematic analysis and benchmark interpretation

## Arguments
- `[target]` - URL, file, or component to benchmark
- `--metrics` - Specific metrics to collect
  - `performance`: Load times, Core Web Vitals, resource usage
  - `accessibility`: WCAG compliance, screen reader compatibility
  - `seo`: Search engine optimization metrics
  - `all`: Comprehensive metric collection
- `--compare <baseline>` - Compare against baseline measurements
- `--export <path>` - Save detailed results to file

## Performance Metrics

### Core Web Vitals
- **LCP (Largest Contentful Paint)**: Loading performance
- **FID (First Input Delay)**: Interactivity responsiveness
- **CLS (Cumulative Layout Shift)**: Visual stability
- **FCP (First Contentful Paint)**: Initial render time
- **TTI (Time to Interactive)**: Full interactivity timing

### Resource Metrics
- **Bundle Size**: JavaScript, CSS, and asset sizes
- **Network Usage**: Request count, data transfer, caching efficiency
- **Memory Usage**: Heap size, memory leaks, garbage collection
- **CPU Usage**: Main thread blocking, script execution time

### User Experience Metrics
- **Load Time**: Full page load on 3G/4G/WiFi
- **Render Performance**: Frame rate, paint times
- **Interaction Response**: Click, scroll, input responsiveness
- **Error Rates**: JavaScript errors, failed requests

## Accessibility Metrics
- **WCAG Compliance**: AA/AAA standard validation
- **Color Contrast**: Text readability assessment
- **Keyboard Navigation**: Tab order and accessibility
- **Screen Reader**: Semantic markup and ARIA labels
- **Focus Management**: Visible focus indicators

## SEO Metrics
- **Page Speed Score**: Google PageSpeed insights
- **Mobile Friendliness**: Responsive design validation
- **Meta Tags**: Title, description, structured data
- **Content Analysis**: Headings, keywords, readability
- **Technical SEO**: Sitemap, robots.txt, crawlability

## Benchmark Types

### Single Page Analysis
- Complete performance audit of individual pages
- Detailed breakdown of loading phases
- Resource waterfall analysis
- Optimization recommendations

### Comparative Analysis
- Before/after performance comparison
- A/B testing results analysis
- Framework performance comparison
- Device and browser performance variance

### Load Testing
- Concurrent user simulation
- Server response under load
- Database performance impact
- CDN and caching effectiveness

## Examples
```bash
# Comprehensive performance benchmark
/wd:benchmark https://myapp.com --metrics all --export ./performance-report.json

# Compare against baseline
/wd:benchmark src/components/Dashboard.tsx --metrics performance --compare ./baseline.json

# Accessibility-focused audit
/wd:benchmark https://myapp.com/signup --metrics accessibility --export ./a11y-report.md

# SEO analysis
/wd:benchmark https://myapp.com --metrics seo
```

## Report Features

### Visual Reports
- **Performance Charts**: Timeline visualization of metrics
- **Waterfall Diagrams**: Resource loading sequence
- **Heat Maps**: User interaction patterns
- **Trend Analysis**: Performance over time

### Actionable Insights
- **Priority Recommendations**: High-impact optimizations
- **Code Splitting Opportunities**: Bundle size reduction
- **Image Optimization**: Format and compression suggestions
- **Caching Strategies**: Browser and CDN optimization

### Comparative Analysis
- **Before/After Metrics**: Improvement quantification
- **Industry Benchmarks**: Performance percentile ranking
- **Competitor Analysis**: Performance comparison
- **Device Performance**: Mobile vs desktop metrics

## Integration Features
- **CI/CD Integration**: Automated performance monitoring
- **Alert Thresholds**: Performance regression detection
- **Historical Tracking**: Performance trend monitoring
- **Team Dashboards**: Shared performance insights

## Output Formats
- **JSON**: Machine-readable metrics data
- **HTML**: Interactive visual reports
- **PDF**: Executive summary reports
- **CSV**: Raw data for analysis
- **Markdown**: Documentation-friendly format