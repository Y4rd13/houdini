import { ZoomMtg } from "@zoomus/websdk";

ZoomMtg.preLoadWasm();
ZoomMtg.prepareJssdk();

var signatureEndpoint = "http://localhost:8000";
var apiKey = "JWT_API_KEY";
var meetingNumber = 123456789;
var role = 0;
var leaveUrl = "http://localhost:8000";
var userName = "WebSDK";
var userEmail = "";
var passWord = "";

