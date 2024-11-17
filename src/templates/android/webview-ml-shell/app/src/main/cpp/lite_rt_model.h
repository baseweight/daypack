#include "tensorflow/lite/c/c_api.h"
#include <string>

class LiteRTModel {

    public:
    LiteRTModel(std::string modelPath);
    ~LiteRTModel();
    private:
    // Not thrilled about using raw pointers here, however LiteRT controls
    // the lifecycle here, and I don't want to use the STL and have them blow up
    TfLiteModel * model;
    TfLiteInterpreterOptions * mOptions;
    TfLiteInterpreter* interpreter;
    TfLiteDelegate* delegate = nullptr;
}