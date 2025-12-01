import 'package:flutter/material.dart';
import '../Bars/header_footer.dart';
import '../Widgets/elevated_button.dart';
import '../Routers/routing_point.dart';

class TermsAgreementPage extends StatefulWidget {
  const TermsAgreementPage({super.key});

  @override
  State<TermsAgreementPage> createState() => _TermsAgreementPageState();
}

class _TermsAgreementPageState extends State<TermsAgreementPage> {
  bool agreeService = false;
  bool agreePersonal = false;
  bool agreeSensitive = false;
  bool agreeImage = false;
  bool agreeAIDisclaimer = false;

  bool agreeAll = false;

  void toggleAgreeAll(bool? value) {
    setState(() {
      agreeAll = value ?? false;
      agreeService = agreeAll;
      agreePersonal = agreeAll;
      agreeSensitive = agreeAll;
      agreeImage = agreeAll;
      agreeAIDisclaimer = agreeAll;
    });
  }

  bool get allChecked =>
      agreeService &&
          agreePersonal &&
          agreeSensitive &&
          agreeImage &&
          agreeAIDisclaimer;

  void toggleSingle() {
    setState(() => agreeAll = allChecked);
  }

  Widget buildTermItem({
    required String title,
    required bool value,
    required Function(bool?) onChanged,
    required String content,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        CheckboxListTile(
          title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
          value: value,
          onChanged: onChanged,
          controlAffinity: ListTileControlAffinity.leading,
        ),

        Padding(
          padding: const EdgeInsets.only(left: 50, right: 10, bottom: 20),
          child: Text(
            content,
            style: const TextStyle(fontSize: 13, height: 1.4, color: Colors.black87),
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const DeepGuardHeader(
        showBack: false,
        showHelp: false,
      ),
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "Terms & Conditions",
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 20),

              // ============================
              // 전체 동의
              // ============================
              CheckboxListTile(
                title: const Text(
                  "Agree to All",
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                value: agreeAll,
                onChanged: toggleAgreeAll,
                controlAffinity: ListTileControlAffinity.leading,
              ),

              const SizedBox(height: 20),

              // ============================
              // 1. 서비스 이용 약관
              // ============================
              buildTermItem(
                title: "1. 서비스 이용 약관 동의",
                value: agreeService,
                onChanged: (v) {
                  setState(() => agreeService = v ?? false);
                  toggleSingle();
                },
                content: """
• 본 서비스는 사용자가 업로드한 이미지에 대해 딥페이크 여부를 분석하고 결과를 제공합니다.
• 또한 본 서비스는 타인의 사진의 무단 업로드에 대한 법적 분쟁 발생 시, 이에 대한 책임을 지지 않음을 명시합니다.
• 서비스 사용자의 상업적 목적의 사용을 금합니다.
• 서비스는 분석 결과 제공, 수사기관 신고 외의 기능을 제공하지 않습니다.
• 일시적 장애나 점검으로 서비스 이용이 제한될 수 있습니다.
• 향후 업데이트로 기능이 변경될 수 있습니다.
• 악성 코드 삽입 등 시스템 악용 행위는 금지됩니다.
• 본 약관에 동의하지 않는 경우 서비스 이용이 제한됩니다.
""",
              ),

              // ============================
              // 2. 개인정보 수집·이용 동의
              // ============================
              buildTermItem(
                title: "2. 개인정보 수집·이용 동의",
                value: agreePersonal,
                onChanged: (v) {
                  setState(() => agreePersonal = v ?? false);
                  toggleSingle();
                },
                content: """
• 본 서비스는 분석을 위해 사용자가 업로드한 이미지 파일을 수집합니다.
• 이미지 외 추가적인 개인정보는 수집하지 않습니다.
• 이미지는 분석 외의 목적으로 사용되지 않습니다.
• 서비스 개선을 위한 최소한의 개인 식별용 정보가 수집될 수 있습니다.
• 상기한 정보에는 개인의 구체적인 정보가 포함되지 않습니다.
• 본 약관에 동의하지 않는 경우 서비스 이용이 제한됩니다.
""",
              ),

              // ============================
              // 3. 민감정보(얼굴 이미지) 처리 동의
              // ============================
              buildTermItem(
                title: "3. 민감정보(얼굴 이미지) 처리 동의",
                value: agreeSensitive,
                onChanged: (v) {
                  setState(() => agreeSensitive = v ?? false);
                  toggleSingle();
                },
                content: """
• 얼굴 이미지가 포함될 수 있으며 이는 민감정보에 해당합니다.
• 이미지 분석 모델이 가동되는 동안 사용자가 업로드한 이미지가 일시적으로 처리됩니다.
• 분석에 사용되는 이미지는 분석 즉시 삭제됩니다.
• 분석에 사용되는 이미지는 제3자에게 제공되지 않습니다.
• 분석에 사용되는 이미지는 법령을 준수하여 안전하게 처리됩니다.
• 분석에 사용되는 이미지는 학습·연구 용도로 활용되지 않습니다.
• 본 약관에 동의하지 않는 경우 서비스 이용이 제한됩니다.
""",
              ),

              // ============================
              // 4. 이미지 업로드·전송·분석 동의
              // ============================
              buildTermItem(
                title: "4. 이미지 업로드·전송·분석 동의",
                value: agreeImage,
                onChanged: (v) {
                  setState(() => agreeImage = v ?? false);
                  toggleSingle();
                },
                content: """
• 이미지는 분석을 위해 사용자가 업로드한 이미지가 서버로 전송됩니다.
• 이미지를 전송하고 처리하는 과정에서 지연이 발생할 수 있습니다.
• 이미지는 딥페이크 모델에 적합한 방식으로 전처리를 진행한 이후 AI 모델로 전달됩니다.
• 전송 및 연산은 암호화된 환경에서 진행됩니다.
• 분석 결과는 사용자의 개인 디바이스로 반환됩니다.
• 분석에 활용된 이미지는 서버에 저장되지 않고 즉시 폐기됩니다.
• 이미지 내용을 확인하지 않습니다.
• 확장자·사이즈 제한이 적용될 수 있습니다.
• 본 약관에 동의하지 않는 경우 서비스 이용이 제한됩니다.
""",
              ),

              // ============================
              // 5. AI 분석 결과의 정확성 비보장 및 면책
              // ============================
              buildTermItem(
                title: "5. AI 분석 결과 정확성 비보장 및 면책",
                value: agreeAIDisclaimer,
                onChanged: (v) {
                  setState(() => agreeAIDisclaimer = v ?? false);
                  toggleSingle();
                },
                content: """
• AI 분석 결과는 100% 정확성을 보장하지 않습니다.
• 결과는 참고용이며 최종 판단 책임은 사용자에게 있습니다.
• 촬영 환경, 이미지 품질 등에 따라 결과가 달라질 수 있습니다.
• 결과를 근거로 한 법적 판단·신고는 사용자 책임이며 본 서비스의 분석 결과는 법적 신고 근거로써의 효력을 가지지 못합니다.
• 알고리즘 업데이트 및 분석 모델 변경에 따라 정확도가 변동될 수 있습니다.
• 분석 결과를 임의로 수정하고 조작하지 않습니다.
• 서버 점검 및 오류 등의 원인으로 분석 실패 시 동일한 이미지를 다시 분석할 수 있습니다.
• 본 약관에 동의하지 않는 경우 서비스 이용이 제한됩니다.
""",
              ),

              const SizedBox(height: 20),

              // ============================
              // 버튼
              // ============================
              CustomElevatedButton(
                text: "Get Agreements",
                backgroundColor: allChecked ? Colors.blue : Colors.grey,
                textColor: Colors.white,
                width: double.infinity,
                fontSize: 16,
                onPressed: allChecked
                    ? () {
                  // 약관 동의 시 서버에 결과 전송 및 한 번 동의하면 자동으로 업로드 페이지로 라우팅
                  Navigator.push(
                    context,
                    RoutingPoint.generateRoute(
                      settings: RouteSettings(name: RoutingPoint.upload),
                    ),
                  );
                }
                    : null,
              ),

              const SizedBox(height: 40),
            ],
          ),
        ),
      ),
    );
  }
}
