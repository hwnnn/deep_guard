import 'package:deep_guard_fe/Services/request_to_server.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../Bars/header_footer.dart';
import '../Routers/endpoint.dart';
import '../Routers/routing_point.dart';
import '../Bars/navigation.dart';
import '../Widgets/elevated_button.dart';
import '../Widgets/reusable_widgets.dart';
import '../Services/request_to_server.dart';

class DetectionResultPage extends StatelessWidget {
  final Map<String, dynamic> result;
  final XFile uploadedImage;

  DetectionResultPage({
    super.key,
    required this.result,
    required this.uploadedImage
  });

  void _toUploadPage(BuildContext context){
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
        // 콜백 실행 시 업로드 페이지로 진입
        onBack: (){
          _toUploadPage(context);
        }
      ),

      bottomNavigationBar: BottomNavBar(
        selectedIndex: 0,
        onTap: (i) {
          if (i == 0){
            _toUploadPage(context);
          }
        },
      ),

      backgroundColor: Colors.white,

      body: Container(
        alignment: Alignment.center,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [

              // ---------- 결과 텍스트 ----------
              const SizedBox(height: 10),
              Text(
                this.result['detection_result']['is_fake'] ? "DeepFake" : "Real Img",
                style: TextStyle(
                  fontSize: 38,
                  color: this.result['detection_result']['is_fake'] ? Colors.red : Colors.green,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 20),

              Container(
                padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 8),
                decoration: BoxDecoration(
                  color: Colors.grey[600],
                  borderRadius: BorderRadius.circular(25),
                ),
                child: Text(
                  "Confidence: ${(this.result['detection_result']['confidence'] * 100).toStringAsFixed(1)}%",
                  style: const TextStyle(
                    fontSize: 26,
                    color: Colors.greenAccent,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),

              const SizedBox(height: 40),

              ImageBox(
                title: "Image",
                description: "",
                uploadedImage: this.uploadedImage,
                onUploadTap: () {},
              ),

              const Spacer(),

              // ---------- 아래 화살표 ----------
              const Icon(Icons.keyboard_arrow_down,
                size: 32,
                color: Colors.deepPurple,
              ),

              const SizedBox(height: 8),
            ],
          ),
        ),
      )
    );
  }
}