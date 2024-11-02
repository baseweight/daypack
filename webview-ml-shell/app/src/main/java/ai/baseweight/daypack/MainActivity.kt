package ai.baseweight.daypack

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import ai.baseweight.daypack.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        binding.webview.settings.javaScriptEnabled = true
        binding.webview.addJavascriptInterface(WebAppInterface(this), "AndroidMLExec")
        setContentView(binding.root);
        binding.webview.loadUrl(resources.getString(R.string.launch_url))
        
    }

    /**
     * A native method that is implemented by the 'daypack' native library,
     * which is packaged with this application.
     */
    external fun stringFromJNI(): String

    companion object {
        // Used to load the 'daypack' library on application startup.
        init {
            System.loadLibrary("daypack")
        }
    }

    // Add this class
    class WebAppInterface(private val context: MainActivity) {
        @JavascriptInterface
        fun stringFromJNI(): String {
            return context.stringFromJNI()
        }
        
        @JavascriptInterface
        fun getInstalledModels(callback: String) {
            // TODO: Implement native model listing
            val models = arrayOf<String>()
            val jsonModels = JSONArray(models)
            binding.webview.evaluateJavascript("$callback($jsonModels)", null)
        }

        @JavascriptInterface 
        fun isModelInstalled(modelId: String, callback: String) {
            // TODO: Implement model existence check
            val installed = false
            binding.webview.evaluateJavascript("$callback($installed)", null)
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
            binding.webview.evaluateJavascript("$callback($metadata)", null)
        }

        @JavascriptInterface
        fun callModel(modelId: String, inputs: String, callback: String) {
            val inputsJson = JSONObject(inputs)

            // TODO: Call the ML model
            // Convert input JSON to byte arrays
            val inputArrays = Array(inputsJson.length()) { i ->
                val input = inputsJson.getString(i)
                input.toByteArray()
            }

            // Call native inference method
            val outputArrays = callModelNative(modelId, inputArrays)

            // Convert output byte arrays back to JSON
            for (i in 0 until outputArrays.size) {
                val output = String(outputArrays[i])
                outputs.put(i.toString(), output)
            }

            val outputs = JSONObject()
            binding.webview.evaluateJavascript("$callback($outputs)", null)
        }
    }

}