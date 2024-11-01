/**
 * DayPack JavaScript Interface
 * Provides TypeScript function signatures for interacting with native device capabilities
 */

interface DayPackInterface {
   
    /**
     * Get list of installed models on device
     * @param callback Callback with array of installed model IDs
     */
    getInstalledModels(callback: (models: string[]) => void): void;

    /**
     * Check if a specific model is installed
     * @param modelId Unique identifier of model to check
     * @param callback Callback with boolean indicating if installed
     */
    isModelInstalled(modelId: string, callback: (installed: boolean) => void): void;

    /**
     * Get metadata for a specific model
     * @param modelId Unique identifier of model to query
     * @param callback Callback with model metadata object containing model details
     */
    getModelMetadata(modelId: string, callback: (metadata: {
        name: string,
        path: string,
        type: string,
        inputs: Array<{
            name: string,
            dtype: string,
            shape: number[]
        }>,
        outputs: Array<{
            name: string, 
            dtype: string,
            shape: number[]
        }>
    }) => void): void;

    /**
     * Call a model with input data
     * @param modelId Unique identifier of model to run
     * @param inputs Object containing input data matching model metadata input schema
     * @param callback Callback with model outputs matching metadata output schema
     */
    callModel(modelId: string, inputs: {[key: string]: any}, callback: (outputs: {[key: string]: any}) => void): void;
}

declare global {
    interface Navigator {
        daypack: DayPackInterface
    }
}
