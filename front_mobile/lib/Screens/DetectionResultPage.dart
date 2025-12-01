import 'dart:convert';

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
                  processedImage: base64Decode(widget.result['detection_result']['result_img']),
                  uploadedImage: this.uploadedImage,
                  onUploadTap: (){},
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
                          "딥페이크 이미지의 특징\n"
                          "물리적 아티팩트\n"
                          "얼굴 경계 블렌딩 불완전\n"
                          "조명 불일치 (얼굴 vs 배경)\n"
                          "피부 텍스처 과도한 스무딩\n"
                          "생리학적 비정상\n"
                          "눈 깜빡임 부족/부자연스러움\n"
                          "치아 형태 왜곡\n"
                          "입술 동기화 오류 (립싱크)\n"
                          "주파수 특성\n"
                          "고주파 디테일 손실\n"
                          "색상 채널 간 불일치\n"
                          "압축 아티팩트 패턴 차이\n"
                          "모델이 주목하는 영역\n"
                          "입 주변 (립싱크 오류)\n"
                          "눈/눈썹 (표정 불일치)\n"
                          "얼굴 경계 (블렌딩 실패)\n"
                          "치아/혀 (생성 어려운 부위)\n"
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
