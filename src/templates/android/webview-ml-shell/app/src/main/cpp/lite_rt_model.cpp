// TFLite C API
#include "tensorflow/lite/c/c_api.h"
#include <android/log.h>

#define PRE_TAG "Model Handler Code"
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR,    PRE_TAG, __VA_ARGS__)

LiteRTModel::LiteRTModel(const char* modelPath) {
    model = TfLiteModelCreateFromFile(fullPath.c_str());
    mOptions = TfLiteInterpreterOptionsCreate();

    if(getDevice() == MLStats::Device::NNAPI)
    {
        TfLiteNnapiDelegateOptions options = TfLiteNnapiDelegateOptionsDefault();
        delegate = TfLiteNnapiDelegateCreate(&options);
        TfLiteInterpreterOptionsAddDelegate(mOptions, delegate);
    }
    else if(getDevice() == MLStats::Device::GPU)
    {
        TfLiteGpuDelegateOptionsV2 options = TfLiteGpuDelegateOptionsV2Default();
        delegate = TfLiteGpuDelegateV2Create(&options);
        TfLiteInterpreterOptionsAddDelegate(mOptions, delegate);
    }
}


LiteRTModel::~LiteRTModel() {
    TfLiteInterpreterDelete(interpreter);
    TfLiteInterpreterOptionsDelete(mOptions);
    if(delegate != nullptr)
    {
        if(getDevice() == MLStats::Device::NNAPI)
        {
            TfLiteNnapiDelegateDelete(delegate);
        }
        else
        {
            TfLiteGpuDelegateV2Delete(delegate);
        }
    }

    TfLiteModelDelete(model);
}
