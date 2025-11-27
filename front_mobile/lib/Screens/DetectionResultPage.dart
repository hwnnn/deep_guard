import 'package:flutter/material.dart';
import '../Bars/header_footer.dart';
import '../Routers/routing_point.dart';
import '../Bars/navigation.dart';
import '../Widgets/elevated_button.dart';
import '../Widgets/reusable_widgets.dart';

class DetectionResultPage extends StatelessWidget {
  final String resultText; // ex: "DeepFake"
  final double confidence; // ex: 0.95

  const DetectionResultPage({
    super.key,
    required this.resultText,
    required this.confidence,
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
                resultText,
                style: const TextStyle(
                  fontSize: 38,
                  color: Colors.red,
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
                  "Confidence: ${(confidence * 100).toStringAsFixed(1)}%",
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
                uploadedImage: const AssetImage("assets/sample_orig.png"),
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