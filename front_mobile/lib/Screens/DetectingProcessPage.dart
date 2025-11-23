import 'package:flutter/material.dart';
import '../Bars/header_footer.dart';
import '../Bars/navigation.dart';
import '../Widgets/elevated_button.dart';
import '../Routers/routing_point.dart';

class DetectingPage extends StatelessWidget{

  const DetectingPage({super.key});

  Widget build(BuildContext context){
    return Scaffold(
      appBar: DeepGuardHeader(
        showBack: false,
        showHelp: false,
        onBack: (){},
      ),
      backgroundColor: Colors.white,

      body: Container(
        alignment: Alignment.center,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            const SizedBox(height: 60),
            const Text(
              'Analyzing...',
              style: TextStyle(
                fontSize: 48,
                fontWeight: FontWeight.bold,
                color: Colors.black,
              ),
            ),
            const SizedBox(height: 60),
            Image(
              image: const AssetImage('assets/analyzing_icons/analyzing.png'),
            ),
            CustomElevatedButton(
                text: 'Debuggingtest',
                textColor: Colors.white,
                fontSize: 16,
                backgroundColor: Colors.blue,
                width: MediaQuery.sizeOf(context).width * 0.5,
                onPressed: (){
                  Navigator.push(
                    context,
                    RoutingPoint.generateRoute(
                        settings: const RouteSettings(
                            name: RoutingPoint.detectionsuccessed
                        )
                    )
                  );
                }
            )
          ],
        )
      )
    );
  }
}

class DetectionSuccessedPage extends StatelessWidget{

  const DetectionSuccessedPage({super.key});

  Widget build(BuildContext context){
    return Scaffold(
        appBar: DeepGuardHeader(
          showBack: false,
          showHelp: false,
          onBack: (){},
        ),
        backgroundColor: Colors.white,

        body: Container(
            alignment: Alignment.center,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                const SizedBox(height: 60),
                const Text(
                  'Analyzing\nSuccessed',
                  style: TextStyle(
                    fontSize: 48,
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 60),
                Image(
                  image: const AssetImage('assets/analyzing_animations/successed.gif'),
                ),
                CustomElevatedButton(
                    text: 'Show Report',
                    textColor: Colors.white,
                    fontSize: 16,
                    backgroundColor: Colors.blue,
                    width: MediaQuery.sizeOf(context).width * 0.5,
                    onPressed: (){
                      Navigator.push(
                          context,
                          RoutingPoint.generateRoute(
                              settings: const RouteSettings(
                                  name: RoutingPoint.detectionresult
                              )
                          )
                      );
                    }
                )
              ],
            )
        )
    );
  }
}

class DetectionFailedPage extends StatelessWidget{

  const DetectionFailedPage({super.key});

  Widget build(BuildContext context){
    return Scaffold(
        appBar: DeepGuardHeader(
          showBack: false,
          showHelp: false,
          onBack: (){},
        ),
        backgroundColor: Colors.white,

        body: Container(
            alignment: Alignment.center,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                const SizedBox(height: 60),
                const Text(
                  'Analyzing\nFailed',
                  style: TextStyle(
                    fontSize: 48,
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 60),
                Image(
                  image: const AssetImage('assets/analyzing_animations/failed.gif'),
                ),
                CustomElevatedButton(
                    text: 'Retry',
                    textColor: Colors.white,
                    fontSize: 16,
                    backgroundColor: Colors.blue,
                    width: MediaQuery.sizeOf(context).width * 0.5,
                    onPressed: (){
                      Navigator.push(
                          context,
                          RoutingPoint.generateRoute(
                              settings: const RouteSettings(
                                  name: RoutingPoint.detecting
                              )
                          )
                      );
                    }
                )
              ],
            )
        )
    );
  }
}
