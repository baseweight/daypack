package ai.baseweight.daypack

class Model() {
    private val name: String
    private val path: String
    private val type: String
    private val inputs: List<String>
    private val outputs: List<String>
}

class ModelManager() {
    private val models = mutableMapOf<String, String>()

}