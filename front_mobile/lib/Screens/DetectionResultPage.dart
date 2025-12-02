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

  void _showReportDialog(BuildContext context) {
    showDialog(
      context: context,
      barrierDismissible: true, // 바깥 터치 시 닫히게 할지 여부
      builder: (context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),

          title: const Text(
            "Report Guide",
            style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold
            ),
          ),

          content: const SingleChildScrollView(
            child: Text(
              "1단계. 긴급 피해 발생 시 즉시 신고\n"
              "영상이 유포 중이거나 협박, 금전 요구, 명예훼손 등 즉각적인 피해가 발생한 경우, 112로 즉시 신고하세요.\n"
              "가까운 경찰서 사이버수사팀을 직접 방문하거나 사이버범죄 신고시스템\n"
              "(ecrm.police.go.kr)을 통해 온라인으로도 신고 가능합니다.\n"
              "신고 시에는 영상 URL, 채팅 내용, 캡처 등 가능한 많은 증거를 확보해야 합니다.\n"
              "2단계. 영상 삭제 및 상담 지원 요청\n"
              "불법 촬영물 또는 딥페이크 영상이 온라인상에 게시된 경우, 디지털성범죄 피해자 지원\n"
              "센터를 통해 삭제·차단 요청 및 법률·심리 상담 요청이 가능합니다.\n"
              "전문 상담원이 1:1로 지원하며, 피해자 본인뿐 아니라 가족·지인도 상담할 수 있습니다.\n"
              "전화: 02-735-8994\n"
              "홈페이지: www.digital-sexcrime.kr\n"
              "운영시간: 평일 09:00~18:00 (주말·공휴일 휴무)\n",
                style: TextStyle(
                fontSize: 16,
                height: 1.4,
                color: Colors.black87,
              ),
            ),
          ),

          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text(
                "Close",
                style: TextStyle(fontSize: 16),
              ),
            )
          ],
        );
      },
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
                  processedImage: widget.result['detection_result']['is_fake'] ? base64Decode(widget.result['detection_result']['result_img']) : null,
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
                                text: 'Report',
                                textColor: Colors.white,
                                fontSize: 16,
                                backgroundColor: Colors.blue,
                                width: MediaQuery.sizeOf(context).width * 0.5,
                                onPressed: (){
                                  _showReportDialog(context);
                                }
                            )
                        ),

                        const SizedBox(height: 10),

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
