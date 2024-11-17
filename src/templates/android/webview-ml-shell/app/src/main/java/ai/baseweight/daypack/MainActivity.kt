package ai.baseweight.daypack

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import ai.baseweight.daypack.databinding.ActivityMainBinding
import android.webkit.JavascriptInterface
import com.google.android.gms.tasks.Task
import com.google.android.gms.tflite.java.TfLiteNative
import org.json.JSONArray
import org.json.JSONObject

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val tfLiteInitializeTask: Task = TfLiteNative.initialize(this)

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

    external fun isModelLoaded(modelId: String) : Boolean
    external fun callModel(
        inputNames: Array<String>,
        inputShapes: Array<IntArray>,
        inputBuffers: Array<ByteArray>,
        outputNames: Array<String>, 
        outputShapes: Array<IntArray>,
        outputBuffers: Array<ByteArray>
    )

    companion object {
        // Used to load the 'daypack' library on application startup.
        init {
            System.loadLibrary("tflite-jni")
            System.loadLibrary("daypack")
        }
    }

    // Add this class
    class WebAppInterface(private val context: MainActivity) {
        
        @JavascriptInterface
        fun getInstalledModels(callback: String) {
            // TODO: Implement native model listing
            val models = arrayOf<String>()
            val jsonModels = JSONArray(models)
            context.binding.webview.evaluateJavascript("$callback($jsonModels)", null)
        }

        @JavascriptInterface
        fun getLoadedModels(callback: String) {
            // TODO: Implement native model listing
            val models = arrayOf<String>()
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