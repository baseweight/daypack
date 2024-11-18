package ai.baseweight.daypack

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import ai.baseweight.daypack.databinding.ActivityMainBinding
import android.webkit.JavascriptInterface
import org.json.JSONArray
import org.json.JSONObject

import kotlinx.coroutines.*

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    val modelManager = ModelManager(this)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        startDownloadThread()

        binding = ActivityMainBinding.inflate(layoutInflater)
        binding.webview.settings.javaScriptEnabled = true
        binding.webview.addJavascriptInterface(WebAppInterface(this), "AndroidMLExec")
        setContentView(binding.root);
        binding.webview.loadUrl(resources.getString(R.string.launch_url))
    }

    fun startDownloadThread() = runBlocking {
        val job = withContext(Dispatchers.IO) {
            modelManager.downloadModels()
        }
    }

    /**
     * A native method that is implemented by the 'daypack' native library,
     * which is packaged with this application.
     */
    external fun loadModel(modelId: String, path: String) : Boolean
    external fun isModelLoaded(modelId: String) : Boolean
    external fun callModel(
        inputNames: Array<String>,
        inputShapes: Array<IntArray>,
        inputBuffers: Array<ByteArray>,
        numInputs: Int,
        outputNames: Array<String>, 
        outputShapes: Array<IntArray>,
        outputBuffers: Array<ByteArray>,
        numOutputs: Int
    )

    companion object {
        // Used to load the 'daypack' library on application startup.
        init {
            System.loadLibrary("daypack")
        }
    }

    // Add this class
    class WebAppInterface(private val context: MainActivity) {
        
        @JavascriptInterface
        fun getInstalledModels(callback: String) {
            val jsonModels = context.modelManager.getInstalledModels()
            context.binding.webview.evaluateJavascript("$callback($jsonModels)", null)
        }

        @JavascriptInterface
        fun getLoadedModels(callback: String) {

            val jsonModels = JSONArray(models)
            context.binding.webview.evaluateJavascript("$callback($jsonModels)", null)
        }

        @JavascriptInterface 
        fun isModelInstalled(modelId: String, callback: String) {
            // TODO: Implement model existence check
            val installed = false
            context.binding.webview.evaluateJavascript("$callback($installed)", null)
        }

        @JavascriptInterface
        fun getModelMetadata(modelId: String, callback: String) {
            // TODO: Implement metadata retrieval
            val metadata = JSONObject().apply {
                put("name", "")
                put("path", "")
                put("type", "")
                put("inputs", JSONArray())
                put("outputs", JSONArray()) 
            }
            context.binding.webview.evaluateJavascript("$callback($metadata)", null)
        }

        @JavascriptInterface
        fun callModel(modelId: String, inputs: String, callback: String) {
            val inputsJson = JSONObject(inputs)
            
            val outputs = JSONObject()
            context.binding.webview.evaluateJavascript("$callback($outputs)", null)
        }
    }

}