import 'package:flutter/material.dart';
import '../Bars/header_footer.dart';
import '../Widgets/elevated_button.dart';
import '../Routers/routing_point.dart';

class LandingPage extends StatelessWidget {
  final String title;
  const LandingPage({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    // 뒤로가기 X, 도움말
    return Scaffold(
      appBar: const AppHeader(
        showBack: false,
        showHelp: false,
      ),
      backgroundColor: Colors.white,
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const SizedBox(height: 30),
            // Sub-title
            const Text(
              "Detect deepfakes with AI",
              style: TextStyle(
                fontSize: 18,
                color: Colors.black54,
              ),
              textAlign: TextAlign.center,
            ),

            const SizedBox(height: 30),

            // 설명 텍스트
            const Text(
              "Our app uses advanced computer vision and deep learning techniques "
                  "to analyze videos and images, identifying subtle inconsistencies "
                  "that indicate manipulation.",
              style: TextStyle(
                fontSize: 16,
                color: Colors.black87,
                height: 1.4,
              ),
              textAlign: TextAlign.center,
            ),

            const Spacer(),

            // Get Started 버튼
            CustomElevatedButton(
              text: "Get Started",
              backgroundColor: Colors.blue,
              textColor: Colors.white,
              width: double.infinity,
              fontSize: 16,
              onPressed: () {
                // TODO: 약관 동의 페이지로 이동 예정
                Navigator.push(
                    context,
                    RoutingPoint.generateRoute(
                        settings: RouteSettings(
                            name: RoutingPoint.termsAgreement
                        )
                    )
                );
              },
            ),

            const SizedBox(height: 40),
          ],
        ),
      ),
    );
  }
}
