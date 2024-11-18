package ai.baseweight.daypack

import android.content.Context
import android.net.Uri
import com.google.gson.Gson

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileOutputStream
import java.io.InputStreamReader
import java.net.URL

class ModelManager(val context: Context) {
    private val models = mutableMapOf<String, ModelMetadata>()

    init {
        try {
            val inputStream = context.assets.open("models/models.json")
            val reader = InputStreamReader(inputStream)
            val modelMetadataList = Gson().fromJson(reader, Array<ModelMetadata>::class.java)
            reader.close()
            inputStream.close()
            modelMetadataList.forEach {
                models[it.name] = it
            }
        }
        catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun getInstalledModels(): String? {
        val metadataList = mutableListOf<ModelMetadata>()
        models.forEach {
            if(it.value?.isInstalled == true) {
                metadataList.add(it.value!!)
            }
        }
        return Gson().toJson(metadataList)
    }



    suspend fun downloadModels()
    {
        models.forEach {
            fetchAndSaveModel(context, Uri.parse(it.value?.path))
            it.value?.isInstalled = true
        }
    }



    suspend fun fetchAndSaveModel(context: Context, modelUri: Uri) {
        withContext(Dispatchers.IO) {
            try {
                val url = URL(modelUri.toString())
                val connection = url.openConnection()
                val inputStream = connection.getInputStream()

                // Save the model to the app's external storage
                val fileName = modelUri.lastPathSegment ?: "model.pte"
                val file = File(context.getExternalFilesDir(null), fileName)
                val outputStream = FileOutputStream(file)

                val buffer = ByteArray(4096)
                var bytesRead: Int

                while (inputStream.read(buffer).also { bytesRead = it } != -1) {
                    outputStream.write(buffer, 0, bytesRead)
                }

                inputStream.close()
                outputStream.close()

                // Model saved successfully
            } catch (e: Exception) {
                // Handle exceptions (e.g., network errors, file I/O errors)
                e.printStackTrace()
            }
        }
    }


}