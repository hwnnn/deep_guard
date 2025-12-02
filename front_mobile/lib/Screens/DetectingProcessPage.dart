import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../Bars/header_footer.dart';
import '../Bars/navigation.dart';
import '../Routers/endpoint.dart';
import '../Services/request_to_server.dart';
import '../Widgets/elevated_button.dart';
import '../Routers/routing_point.dart';
import '../Utils/asset_managers.dart';

class DetectingPage extends StatefulWidget {

  XFile? uploadedImage;
  DetectingPage({super.key, required this.uploadedImage});

  @override
  State<DetectingPage> createState() => _DetectingPageState(uploadedImage: uploadedImage);
}

class _DetectingPageState extends State<DetectingPage> {

  XFile? uploadedImage;
  _DetectingPageState({required this.uploadedImage});

  @override
  void initState() {
    super.initState();
    _startAnalysis(); // 페이지 열리자마자 분석 시작
  }

  Future<void> _startAnalysis() async {
    final String _filepath = uploadedImage!.path;
    final String _filename = _filepath.split('/').last;

    // 확장자 → MIME 타입 변환
    String ext = _filename.split('.').last.toLowerCase();
    String mimetype = 'jpeg';
    if (ext == 'png') mimetype = 'png';
    if (ext == 'gif') mimetype = 'gif';

    final result = await requestToServer(
      taskid: '',
      endpoint: ENDPOINTS['upload']!,
      type: "POST",
      data: {
        'file': await MultipartFile.fromFile(
          _filepath,
          filename: _filename,
          contentType: DioMediaType('image', mimetype),
        ),
      },
      headers: {
        'accept': 'application/json',
        // Content-Type: multipart/form-data
      },
    );

    if (!mounted) return;

    if (result['status'] == 'success') {
      Navigator.pushReplacement(
        context,
        RoutingPoint.generateRoute(
          uploadedImage: this.uploadedImage,
          result: result,
          settings: const RouteSettings(
            name: RoutingPoint.detectionsuccessed,
          ),
        ),
      );
    } else {
      Navigator.pushReplacement(
        context,
        RoutingPoint.generateRoute(
          uploadedImage: this.uploadedImage,
          settings: const RouteSettings(
            name: RoutingPoint.detectionfailed,
          ),
        ),
      );
    }
  }


  @override
  Widget build(BuildContext context) {
    final analyzingicon = AssetsManager.find('analyzing.png');

    return Scaffold(
      appBar: DeepGuardHeader(
        showBack: false,
        showHelp: false,
        onBack: () {},
      ),
      backgroundColor: Colors.white,
      body: Container(
        alignment: Alignment.center,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            const SizedBox(height: 60),
            const Text(
              'Analyzing...',
              style: TextStyle(
                fontSize: 48,
                fontWeight: FontWeight.bold,
                color: Colors.black,
              ),
            ),
            const SizedBox(height: 60),
            Image(
              image: AssetImage(analyzingicon ?? ""),
            ),
            const SizedBox(height: 50),
            const CircularProgressIndicator(
              strokeWidth: 5,
              color: Colors.blue,
            ),
          ],
        ),
      ),
    );
  }
}

class DetectionSuccessedPage extends StatelessWidget{

  final XFile uploadedImage;
  final Map<String, dynamic> result;
  const DetectionSuccessedPage(
      {
        super.key,
        required this.uploadedImage,
        required this.result
      }
  );

  Widget build(BuildContext context){

    final successGif = AssetsManager.find('successed.gif');

    return Scaffold(
        appBar: DeepGuardHeader(
          showBack: false,
          showHelp: false,
          onBack: (){},
        ),
        backgroundColor: Colors.white,

        body: Container(
            alignment: Alignment.center,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                const SizedBox(height: 60),
                const Text(
                  'Analyzing\nSuccessed',
                  style: TextStyle(
                    fontSize: 48,
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 30),
                Image(
                  image: AssetImage(successGif ?? ""),
                ),
                CustomElevatedButton(
                    text: 'Show Report',
                    textColor: Colors.white,
                    fontSize: 16,
                    backgroundColor: Colors.blue,
                    width: MediaQuery.sizeOf(context).width * 0.5,
                    onPressed: () async {
                      String taskid = this.result['task_id'];
                      Map<String, dynamic> detectionResult = await requestToServer(
                          taskid: taskid,
                          endpoint: ENDPOINTS['lookUpResults']!,
                          type: 'GET',
                          data: {},
                          headers: {
                            'accept': 'Content-Type: application/json'
                          }
                      );
                      Navigator.push(
                          context,
                          RoutingPoint.generateRoute(
                              uploadedImage: this.uploadedImage,
                              result: detectionResult,
                              settings: const RouteSettings(
                                  name: RoutingPoint.detectionresult
                              )
                          )
                      );
                    }
                )
              ],
            )
        )
    );
  }
}

class DetectionFailedPage extends StatelessWidget{

  final XFile uploadedImage;
  const DetectionFailedPage({super.key, required this.uploadedImage});

  Widget build(BuildContext context){

    final failedGif = AssetsManager.find('failed.gif');

    return Scaffold(
        appBar: DeepGuardHeader(
          showBack: false,
          showHelp: false,
          onBack: (){},
        ),
        backgroundColor: Colors.white,

        body: Container(
            alignment: Alignment.center,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                const SizedBox(height: 20),
                const Text(
                  'Analyzing\nFailed',
                  style: TextStyle(
                    fontSize: 48,
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 20),
                Image(
                  image: AssetImage(failedGif ?? ""),
                ),
                CustomElevatedButton(
                    text: 'Home',
                    textColor: Colors.white,
                    fontSize: 16,
                    backgroundColor: Colors.blue,
                    width: MediaQuery.sizeOf(context).width * 0.5,
                    onPressed: (){
                      Navigator.push(
                          context,
                          RoutingPoint.generateRoute(
                              // uploadedImage: this.uploadedImage,
                              settings: const RouteSettings(
                                  name: RoutingPoint.upload
                              )
                          )
                      );
                    }
                ),
                const SizedBox(height: 10),
                CustomElevatedButton(
                    text: 'Retry',
                    textColor: Colors.white,
                    fontSize: 16,
                    backgroundColor: Colors.blue,
                    width: MediaQuery.sizeOf(context).width * 0.5,
                    onPressed: (){
                      Navigator.push(
                          context,
                          RoutingPoint.generateRoute(
                              uploadedImage: this.uploadedImage,
                              settings: const RouteSettings(
                                  name: RoutingPoint.detecting
                              )
                          )
                      );
                    }
                )
              ],
            )
        )
    );
  }
}
