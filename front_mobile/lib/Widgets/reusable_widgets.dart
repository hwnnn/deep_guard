import 'package:flutter/material.dart';

/// 1. TitleSection(1, 2번 UI용)
/// 2. ImageBox
/// 3. DetectionResultHeader(3번 UI용)


/// ------------------------------------------------------------
/// 1. 공용 상단 Title Section (Upload Media / Detection Result 등)
/// ------------------------------------------------------------
class TitleSection extends StatelessWidget {
  final String mainTitle;       // Upload Media, Detection Result 등
  final String subTitle;        // Detect deepfakes with AI 등

  const TitleSection({
    super.key,
    required this.mainTitle,
    required this.subTitle,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const SizedBox(height: 20),
        Text(
          mainTitle,
          style: const TextStyle(
            fontSize: 32,
            fontWeight: FontWeight.bold,
          ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 8),
        Text(
          subTitle,
          style: const TextStyle(
            fontSize: 18,
            color: Colors.black54,
          ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 30),
      ],
    );
  }
}

/// ------------------------------------------------------------
/// 2. 업로드용/이미지 표시용 공통 컨테이너
/// ------------------------------------------------------------
/// 업로드 전: 설명 텍스트 + Upload 버튼
/// 업로드 후: 업로드된 이미지 표시 + 상단 title만 유지
/// ------------------------------------------------------------
class ImageBox extends StatelessWidget {
  final String title;                   // Orig Image / DF Image / Tap to upload
  final String description;             // 업로드 전 안내문구
  final ImageProvider? uploadedImage;   // 업로드된 이미지(없으면 null)
  final VoidCallback onUploadTap;       // 업로드 버튼 콜백

  const ImageBox({
    super.key,
    required this.title,
    required this.description,
    this.uploadedImage,
    required this.onUploadTap,
  });

  @override
  Widget build(BuildContext context) {
    final bool hasImage = uploadedImage != null;

    return Container(
      width: 130,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        border: Border.all(color: Colors.black12, width: 2, style: BorderStyle.solid),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        children: [
          Text(
            title,
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
            textAlign: TextAlign.center,
          ),

          const SizedBox(height: 10),

          // 업로드 전 = 설명 표시
          // 업로드 후 = 이미지 표시
          hasImage
              ? ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: Image(
                image: uploadedImage!,
                width: 130,
                height: 180,
                fit: BoxFit.cover,
              ))
              : Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                const SizedBox(
                    height: 40
                ),
                Text(
                  description,
                  style: const TextStyle(fontSize: 12, color: Colors.black54),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(
                    height: 40
                ),
              ],
          ),

          const SizedBox(height: 15),

          // 업로드 버튼은 "업로드 전" 에만 표시
          hasImage
              ? const SizedBox.shrink()
              : ElevatedButton(
            onPressed: onUploadTap,
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.black12,
              elevation: 0,
              padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
            ),
            child: const Text(
              "Upload",
              style: TextStyle(fontSize: 18, color: Colors.black),
            ),
          ),
        ],
      ),
    );
  }
}

/// ------------------------------------------------------------
/// 3. Detection Result 상단 UI (DeepFake / Real + Confidence)
/// ------------------------------------------------------------
class DetectionResultHeader extends StatelessWidget {
  final bool isFake;
  final double confidence;

  const DetectionResultHeader({
    super.key,
    required this.isFake,
    required this.confidence,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          isFake ? "DeepFake" : "Real",
          style: TextStyle(
            fontSize: 40,
            fontWeight: FontWeight.bold,
            color: isFake ? Colors.red : Colors.green,
          ),
        ),
        const SizedBox(height: 10),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
          decoration: BoxDecoration(
            color: Colors.grey.shade400,
            borderRadius: BorderRadius.circular(30),
          ),
          child: Text(
            "Confidence: ${(confidence * 100).toStringAsFixed(0)}%",
            style: TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
              color: Colors.greenAccent.shade700,
            ),
          ),
        ),
        const SizedBox(height: 30),
      ],
    );
  }
}