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
}