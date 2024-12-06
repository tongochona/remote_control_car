#include <WiFi.h>

const char *ssid = "Anh Trai Say Bye"; // Tên mạng Wi-Fi
const char *password = "12345678";    // Mật khẩu mạng Wi-Fi

void setup() {
  // Khởi tạo Serial để theo dõi thông tin
  Serial.begin(115200);
  Serial.println();
  Serial.println("Setting up Access Point...");

  // Thiết lập ESP32 làm Access Point
  if (WiFi.softAP(ssid, password)) {
    Serial.println("Access Point started successfully!");
  } else {
    Serial.println("Failed to start Access Point.");
    while (1); // Dừng chương trình nếu thất bại
  }

  // Hiển thị địa chỉ IP của Access Point
  IPAddress apIP = WiFi.softAPIP();
  Serial.print("AP IP Address: ");
  Serial.println(apIP);
}

void loop() {
  // Lấy số lượng client đang kết nối
  int numClients = WiFi.softAPgetStationNum();

  // Hiển thị số lượng client trên Serial
  Serial.print("Number of clients connected: ");
  Serial.println(numClients);

  // Chờ 2 giây trước khi cập nhật tiếp
  delay(2000);
}
