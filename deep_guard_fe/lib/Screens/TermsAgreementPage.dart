import 'package:flutter/material.dart';
import '../Bars/header_footer.dart';
import '../Routers/routing_point.dart';
import '../Widgets/elevated_button.dart';

class TermsAgreementPage extends StatelessWidget {
  const TermsAgreementPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const AppHeader(
        showBack: false,
        showHelp: false,
      ),
      backgroundColor: Colors.white,
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              "Terms & Conditions",
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.w700,
              ),
            ),
            SizedBox(height: 20),
            Text(
              "Agreements_Terms\n",
              style: TextStyle(fontSize: 16, height: 1.5),
            ),

            const Spacer(),

            // Get Started 버튼
            CustomElevatedButton(
              text: "Get Agreements",
              backgroundColor: Colors.blue,
              textColor: Colors.white,
              width: double.infinity,
              fontSize: 16,
              onPressed: () {
                // Route : Terms Agreement
                Navigator.push(
                  context,
                  RoutingPoint.generateRoute(
                      settings: RouteSettings(
                          name: RoutingPoint.upload
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
