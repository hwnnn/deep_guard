import 'package:flutter/material.dart';

class CustomElevatedButton extends StatelessWidget {
  final String text;
  final Color textColor;
  final double fontSize;
  final Color backgroundColor;
  final double width;
  final VoidCallback? onPressed;  // 버튼 클릭 시 작동할 콜백 함수

  const CustomElevatedButton({
    super.key,
    required this.text,
    required this.textColor,
    required this.fontSize,
    required this.backgroundColor,
    required this.width,
    this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width,
      height: 50, // 기본 높이統一
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: backgroundColor,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
          elevation: 0,
        ),
        onPressed: onPressed,
        child: Text(
          text,
          style: TextStyle(
            color: textColor,
            fontSize: fontSize,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
    );
  }

  // 개별 함수 x
}
