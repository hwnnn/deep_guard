import 'package:deep_guard_fe/Services/request_to_server.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../Bars/header_footer.dart';
import '../Routers/endpoint.dart';
import '../Routers/routing_point.dart';
import '../Bars/navigation.dart';
import '../Widgets/elevated_button.dart';
import '../Widgets/reusable_widgets.dart';

class DetectionResultPage extends StatefulWidget {
  final Map<String, dynamic> result;
  final XFile uploadedImage;

  const DetectionResultPage({
    super.key,
    required this.result,
    required this.uploadedImage
  });

  @override
  State<DetectionResultPage> createState() => _DetectionResultPageState(uploadedImage: this.uploadedImage);
}

class _DetectionResultPageState extends State<DetectionResultPage> {
  bool showDetail = false;
  final XFile? uploadedImage;
  _DetectionResultPageState({required this.uploadedImage});

  void _toUploadPage(BuildContext context) {
    Navigator.push(
      context,
      RoutingPoint.generateRoute(
        settings: const RouteSettings(
          name: RoutingPoint.upload,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: DeepGuardHeader(
        showBack: true,
        showHelp: true,
        onBack: () => _toUploadPage(context),
      ),

      bottomNavigationBar: BottomNavBar(
        selectedIndex: 0,
        onTap: (i) {
          if (i == 0) _toUploadPage(context);
        },
      ),

      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Center(
          child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,

              children: [
                // ---------- 결과 텍스트 ----------
                Text(
                  widget.result['detection_result']['is_fake']
                      ? "DeepFake"
                      : "Real Img",
                  style: TextStyle(
                    fontSize: 38,
                    color: widget.result['detection_result']['is_fake']
                        ? Colors.red
                        : Colors.green,
                    fontWeight: FontWeight.bold,
                  ),
                ),

                const SizedBox(height: 20),

                // ---------- Confidence ----------
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 8),
                  decoration: BoxDecoration(
                    color: Colors.grey[600],
                    borderRadius: BorderRadius.circular(25),
                  ),
                  child: Text(
                    "Confidence: ${(widget.result['detection_result']['confidence'] * 100).toStringAsFixed(1)}%",
                    style: const TextStyle(
                      fontSize: 26,
                      color: Colors.greenAccent,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),

                const SizedBox(height: 40),

                // ---------- Image ----------
                ImageBox(
                  title: "Image",
                  description: "",
                  uploadedImage: widget.uploadedImage,
                  onUploadTap: () {},
                ),

                const SizedBox(height: 20),

                GestureDetector(
                  onTap: () => setState(() => showDetail = !showDetail),
                  child: Icon(
                    showDetail
                        ? Icons.keyboard_arrow_up
                        : Icons.keyboard_arrow_down,
                    size: 38,
                    color: Colors.deepPurple,
                  ),
                ),

                const SizedBox(height: 10),

                if (showDetail)
                  Container(
                    width: MediaQuery.sizeOf(context).width * 0.8,
                    padding: const EdgeInsets.all(16),
                    margin: const EdgeInsets.only(bottom: 40),
                    decoration: BoxDecoration(
                      color: Colors.grey.shade200,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "Detection Result",
                          style: const TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          "\n"
                          "얼굴 경계선 분석 정상\n"
                          "조명 반사량 균형\n"
                          "프레임 간 노이즈 미검출\n"
                          "GAN 흔적 없음\n"
                          "얼굴 특징점 비율 정상\n"
                          "전반적으로 정상 이미지로 판단됨\n"
                          "전반적으로 정상 이미지로 판단됨\n"
                          "전반적으로 정상 이미지로 판단됨\n"
                          "전반적으로 정상 이미지로 판단됨\n"
                          "전반적으로 정상 이미지로 판단됨\n"
                          "전반적으로 정상 이미지로 판단됨\n"
                          "전반적으로 정상 이미지로 판단됨\n"
                        ),
                        Container(
                          alignment: Alignment.center,
                          child: CustomElevatedButton(
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
                        )
                      ]
                    )
                  ),
              ],
          ),
        ),
      ),
    );
  }
}
