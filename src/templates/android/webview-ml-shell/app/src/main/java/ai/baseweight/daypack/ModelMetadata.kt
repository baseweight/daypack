package ai.baseweight.daypack

class ModelMetadata(val name: String, val path: String,
                    val type: String, val inputs: List<String>,
                    val outputs: List<String>)
{
    var isLoaded: Boolean = false
    var isInstalled: Boolean = false
}
