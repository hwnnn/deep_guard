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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppHeader(
        showBack: true,
        showHelp: false,
      ),

      bottomNavigationBar: BottomNavBar(
        selectedIndex: 0,
        onTap: (i) {},
      ),

      backgroundColor: Colors.white,

      body: Padding(
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

            const SizedBox(height: 5),

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

            const SizedBox(height: 20),

            // ---------- 이미지 2개 박스 ----------
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ImageBox(
                  title: "Orig Image",
                  description: "",
                  uploadedImage: const AssetImage("assets/sample_orig.png"),
                  onUploadTap: () {},
                ),
                ImageBox(
                  title: "DF Image",
                  description: "",
                  uploadedImage: const AssetImage("assets/sample_df.png"),
                  onUploadTap: () {},
                ),
              ],
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
    );
  }
}