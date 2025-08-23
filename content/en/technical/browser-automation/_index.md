---
title: Browser Automation Architecture
description: How AIMatrix connects to web browsers using Chrome DevTools Protocol for intelligent automation
weight: 3
---

# AIMatrix Browser Automation

AIMatrix uses **Chrome DevTools Protocol (CDP)** to provide powerful browser automation capabilities, allowing agents to interact with web applications as naturally as humans do.

## Why CDP Over Other Approaches?

### Our Choice: Chrome DevTools Protocol

After evaluating multiple approaches, we chose CDP because it offers:

1. **Attach to Existing Sessions** - Connect to user's already-open Chrome
2. **Lowest Latency** - Direct WebSocket connection
3. **Full Browser Control** - Access to all Chrome capabilities
4. **No Installation Required** - Works with existing Chrome
5. **User Context Preserved** - Maintains logins, cookies, sessions

### Comparison of Approaches

| Approach | Pros | Cons | Our Use Case |
|----------|------|------|--------------|
| **CDP (Our Choice)** | Attach to running Chrome, full control, low latency | More complex setup | ✅ Perfect for desktop agents |
| Playwright | Simple API, multi-browser | Can't attach to existing Chrome | ❌ Too isolated |
| Extension | Lives in browser, user permissions | Requires installation, review process | ❌ Too restrictive |

## Architecture Overview

```
┌──────────────────────────────────────────┐
│         AIMatrix Console/CLI             │
│          (Compose Multiplatform)         │
└─────────────────┬────────────────────────┘
                  │
         WebSocket Connection
                  │
┌─────────────────▼────────────────────────┐
│            Chrome Browser                │
│     (User's Existing Instance)           │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │   Chrome DevTools Protocol         │  │
│  │   Port: 9222 (configurable)       │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Tabs, DOM, Network, Console, Storage    │
└──────────────────────────────────────────┘
```

## Implementation Details

### Starting Chrome with CDP

When AIMatrix starts, it can either:

1. **Attach to existing Chrome** (preferred)
2. **Launch new Chrome instance** with CDP enabled

```kotlin
// AIMatrix Browser Bridge (Kotlin/Compose)
class BrowserBridge {
    fun connectToChrome(): ChromeConnection {
        // First, try to find existing Chrome with CDP
        val existingPort = findChromeDebugPort()
        if (existingPort != null) {
            return attachToChrome(existingPort)
        }
        
        // Otherwise, launch Chrome with CDP enabled
        return launchChromeWithCDP()
    }
    
    private fun launchChromeWithCDP(): ChromeConnection {
        val port = 9222
        val userDataDir = "${System.getProperty("user.home")}/.aimatrix-chrome"
        
        val process = ProcessBuilder(
            findChromeExecutable(),
            "--remote-debugging-port=$port",
            "--user-data-dir=$userDataDir",
            "--no-first-run",
            "--disable-default-apps"
        ).start()
        
        // Wait for Chrome to be ready
        waitForPort(port)
        
        return ChromeConnection(port)
    }
}
```

### CDP Communication Layer

```kotlin
// WebSocket connection to Chrome
class ChromeConnection(private val port: Int) {
    private val client = HttpClient(CIO) {
        install(WebSockets)
    }
    
    suspend fun connect() {
        // Get WebSocket endpoint
        val targets = client.get("http://localhost:$port/json")
            .bodyAsText()
            .let { Json.parseToJsonElement(it) }
        
        val wsUrl = targets.jsonArray.first()
            .jsonObject["webSocketDebuggerUrl"]!!
            .jsonPrimitive.content
        
        // Connect via WebSocket
        client.webSocket(wsUrl) {
            // Send CDP commands
            send(Frame.Text("""
                {
                    "id": 1,
                    "method": "Page.enable"
                }
            """))
            
            // Handle responses and events
            for (frame in incoming) {
                if (frame is Frame.Text) {
                    handleCDPMessage(frame.readText())
                }
            }
        }
    }
}
```

### High-Level Agent Interface

```kotlin
// What agents actually use (abstracted CDP complexity)
class WebAgent(private val browser: BrowserBridge) {
    
    suspend fun navigateTo(url: String) {
        browser.sendCommand("Page.navigate", mapOf("url" to url))
    }
    
    suspend fun fillForm(selector: String, text: String) {
        // Find element
        val nodeId = browser.querySelector(selector)
        
        // Focus element
        browser.sendCommand("DOM.focus", mapOf("nodeId" to nodeId))
        
        // Type text
        text.forEach { char ->
            browser.sendCommand("Input.dispatchKeyEvent", mapOf(
                "type" to "char",
                "text" to char.toString()
            ))
        }
    }
    
    suspend fun click(selector: String) {
        val rect = browser.getElementRect(selector)
        browser.sendCommand("Input.dispatchMouseEvent", mapOf(
            "type" to "mousePressed",
            "x" to rect.centerX,
            "y" to rect.centerY,
            "button" to "left",
            "clickCount" to 1
        ))
        browser.sendCommand("Input.dispatchMouseEvent", mapOf(
            "type" to "mouseReleased",
            "x" to rect.centerX,
            "y" to rect.centerY,
            "button" to "left"
        ))
    }
    
    suspend fun extractData(jsExpression: String): String {
        val result = browser.sendCommand("Runtime.evaluate", mapOf(
            "expression" to jsExpression,
            "returnByValue" to true
        ))
        return result["result"]["value"].toString()
    }
}
```

## Real-World Use Cases

### 1. Form Automation

```kotlin
// Agent automatically fills complex web forms
class FormFillingAgent(private val web: WebAgent) {
    
    suspend fun processExpenseForm(receipt: Receipt) {
        // Navigate to expense system
        web.navigateTo("https://expenses.company.com")
        
        // Fill form fields
        web.fillForm("#vendor", receipt.vendor)
        web.fillForm("#amount", receipt.amount.toString())
        web.fillForm("#date", receipt.date)
        web.selectDropdown("#category", receipt.category)
        
        // Upload receipt image
        web.uploadFile("#receipt-upload", receipt.imagePath)
        
        // Submit
        web.click("#submit-button")
        
        // Wait for confirmation
        web.waitForElement(".success-message")
    }
}
```

### 2. Data Extraction

```kotlin
// Agent extracts data from any website
class DataExtractionAgent(private val web: WebAgent) {
    
    suspend fun extractTableData(url: String): List<Map<String, String>> {
        web.navigateTo(url)
        
        // Extract using JavaScript in the page context
        val data = web.extractData("""
            Array.from(document.querySelectorAll('table tr')).map(row => {
                const cells = Array.from(row.querySelectorAll('td'));
                return {
                    name: cells[0]?.innerText,
                    value: cells[1]?.innerText,
                    status: cells[2]?.innerText
                };
            });
        """)
        
        return Json.decodeFromString(data)
    }
}
```

### 3. Multi-Tab Orchestration

```kotlin
// Agent manages multiple browser tabs for complex workflows
class MultiTabAgent(private val browser: BrowserBridge) {
    
    suspend fun compareProducts(productName: String) {
        // Open multiple shopping sites
        val amazon = browser.newTab("https://amazon.com")
        val ebay = browser.newTab("https://ebay.com")
        val alibaba = browser.newTab("https://alibaba.com")
        
        // Search on all sites in parallel
        coroutineScope {
            launch { searchOnSite(amazon, productName) }
            launch { searchOnSite(ebay, productName) }
            launch { searchOnSite(alibaba, productName) }
        }
        
        // Extract and compare prices
        val prices = listOf(
            extractPrice(amazon),
            extractPrice(ebay),
            extractPrice(alibaba)
        )
        
        return findBestDeal(prices)
    }
}
```

## Security & Privacy

### User Control

```yaml
# AIMatrix browser permissions
browser:
  permissions:
    # User must explicitly allow
    - domain_whitelist:
      - "*.company.com"
      - "expenses.internal"
    
    # Blocked by default
    - blocked_domains:
      - "*.banking.com"
      - "*.gov"
    
    # Action permissions
    - allow_form_fill: true
    - allow_file_upload: ask_each_time
    - allow_downloads: false
    - allow_payment_forms: false
```

### Secure Communication

```kotlin
// All CDP communication is local only
class SecureBrowserBridge {
    init {
        // Only accept local connections
        require(isLocalhost(cdpHost)) {
            "CDP connection must be localhost only"
        }
        
        // Validate Chrome process
        require(isTrustedChromeProcess()) {
            "Chrome process verification failed"
        }
    }
    
    // Audit all actions
    override suspend fun sendCommand(method: String, params: Map<String, Any>) {
        auditLog.record(
            timestamp = now(),
            method = method,
            params = params.sanitized(),
            user = currentUser()
        )
        
        super.sendCommand(method, params)
    }
}
```

## Advanced Features

### Visual AI Integration

```kotlin
// Combine CDP with vision models
class VisualWebAgent(
    private val web: WebAgent,
    private val vision: VisionModel
) {
    suspend fun clickVisually(description: String) {
        // Take screenshot via CDP
        val screenshot = web.captureScreenshot()
        
        // Use vision model to find element
        val location = vision.findElement(
            image = screenshot,
            description = description  // e.g., "blue submit button"
        )
        
        // Click at coordinates
        web.clickAt(location.x, location.y)
    }
    
    suspend fun understandPage(): PageUnderstanding {
        val screenshot = web.captureScreenshot()
        val dom = web.getDOM()
        
        // Combine visual and DOM understanding
        return vision.analyzePage(
            screenshot = screenshot,
            dom = dom,
            task = "Understand the page structure and purpose"
        )
    }
}
```

### Intelligent Wait Strategies

```kotlin
// Smart waiting without fixed delays
class SmartWaitStrategies {
    
    suspend fun waitForPageReady() {
        // Wait for multiple signals
        web.waitFor(
            allOf(
                networkIdle(500),  // No requests for 500ms
                domStable(1000),   // DOM unchanged for 1s
                jsExpression("document.readyState === 'complete'"),
                noSpinners()       // No loading indicators
            ),
            timeout = 30.seconds
        )
    }
    
    suspend fun waitForAjaxComplete() {
        web.waitFor(
            jsExpression("""
                typeof jQuery !== 'undefined' 
                ? jQuery.active === 0 
                : true
            """)
        )
    }
}
```

### Session Management

```kotlin
// Preserve and restore browser sessions
class SessionManager {
    suspend fun saveSession(name: String) {
        val session = BrowserSession(
            cookies = web.getCookies(),
            localStorage = web.getLocalStorage(),
            sessionStorage = web.getSessionStorage()
        )
        
        secureStore.save(name, session.encrypted())
    }
    
    suspend fun restoreSession(name: String) {
        val session = secureStore.load(name).decrypt()
        
        web.setCookies(session.cookies)
        web.setLocalStorage(session.localStorage)
        web.setSessionStorage(session.sessionStorage)
    }
}
```

## Performance Optimization

### Connection Pooling

```kotlin
// Reuse CDP connections efficiently
object BrowserPool {
    private val connections = mutableMapOf<String, ChromeConnection>()
    
    suspend fun getConnection(profile: String): ChromeConnection {
        return connections.getOrPut(profile) {
            createNewConnection(profile)
        }
    }
    
    fun releaseAll() {
        connections.values.forEach { it.close() }
        connections.clear()
    }
}
```

### Parallel Execution

```kotlin
// Execute browser operations in parallel
class ParallelBrowserOps {
    suspend fun processManyPages(urls: List<String>) = coroutineScope {
        urls.map { url ->
            async {
                val tab = browser.newTab()
                tab.navigate(url)
                tab.extractData()
            }
        }.awaitAll()
    }
}
```

## Debugging & Development

### CDP Inspector

```kotlin
// Built-in CDP debugging tools
class CDPInspector {
    fun enableDebugMode() {
        // Log all CDP messages
        cdpConnection.onMessage { message ->
            logger.debug("CDP: $message")
        }
        
        // Open Chrome DevTools for debugging
        Desktop.browse(URI("http://localhost:9222"))
    }
    
    fun recordSession(filename: String) {
        // Record all CDP traffic for replay
        cdpRecorder.startRecording(filename)
    }
}
```

### Testing Helpers

```kotlin
// Test browser automation locally
class BrowserTestHelper {
    @Test
    fun testFormFilling() = runTest {
        // Launch test Chrome instance
        val browser = BrowserBridge.createTestInstance()
        
        // Create test server
        val server = TestWebServer()
        server.addPage("/form", testFormHtml)
        
        // Test the agent
        val agent = FormFillingAgent(browser)
        agent.fillTestForm(server.url("/form"))
        
        // Verify
        assertEquals("expected", server.getSubmittedData())
    }
}
```

## Integration with Master Agent

```kotlin
// Browser automation as part of Master Agent
class MasterAgent {
    private val browser = BrowserBridge()
    
    suspend fun processWebTask(task: WebTask) {
        when (task.type) {
            "extract_data" -> {
                // Use CDP to extract data
                val data = browser.extractFromPage(task.url, task.selector)
                
                // Process with AI
                val processed = aiModel.process(data)
                
                // Store results
                database.save(processed)
            }
            
            "fill_form" -> {
                // AI determines form values
                val formData = aiModel.prepareFormData(task.context)
                
                // CDP fills the form
                browser.fillForm(task.url, formData)
            }
            
            "monitor_page" -> {
                // CDP watches for changes
                browser.watchPage(task.url) { change ->
                    // AI analyzes changes
                    aiModel.analyzeChange(change)
                }
            }
        }
    }
}
```

## Benefits of CDP Approach

### 🔗 **Seamless Integration**
- Works with user's existing Chrome
- Preserves all logins and sessions
- No separate browser needed

### ⚡ **Real-time Performance**
- Direct WebSocket communication
- No middleware overhead
- Instant response to page changes

### 🛠️ **Full Browser Control**
- Access to all Chrome features
- Network interception
- JavaScript execution
- Cookie management

### 🔒 **Security**
- Runs locally only
- No cloud services required
- Full audit trail
- User permission control

### 🎯 **Reliability**
- Direct browser control (no flaky selectors)
- Handle dynamic content
- Work with any website
- Bypass automation detection

## Getting Started

```bash
# AIMatrix automatically sets up browser bridge
aimatrix init --with-browser

# Test browser connection
aimatrix browser test
> Connecting to Chrome...
> ✓ CDP connection established
> ✓ Can control browser
> ✓ JavaScript execution working

# Run browser agent
aimatrix agent run web-automator
```

---

*AIMatrix Browser Automation - Your AI controls the web*