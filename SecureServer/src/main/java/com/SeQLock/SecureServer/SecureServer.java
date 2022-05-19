package com.SeQLock.SecureServer;

import java.util.ArrayList;
import java.util.List;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.json.JSONArray;
import org.json.JSONObject;
import com.SeQLock.SecureServer.model.User;
import com.SeQLock.SecureServer.utils.SimpleMqttClient;

public class SecureServer {
	private List<User> users = new ArrayList<User>();

	public SecureServer() {
		super();
	}

	public void startup() {
		var client = new SimpleMqttClient("localhost") {
			@Override
			public void messageArrived(String topic, MqttMessage message) throws Exception {
				try {
					System.out.println("Message received at topic " + topic + ": " + message);
					JSONObject requestObject = new JSONObject(message);
					var payload = (JSONArray)requestObject.get("payload");
					var jsonarray = payload.toList();
				
					byte[] bytes = new byte[jsonarray.size()];;
				
					for (var i = 0; i < jsonarray.size(); i++) {
						bytes[i] = (byte)jsonarray.get(i);
					}
				
					String requestBody = new String(bytes);
				
				
					JSONObject requestBodyObject = new JSONObject(requestBody);
				
					var userid = requestBodyObject.get("userid");
					var timestamp = requestBodyObject.get("timestamp");
					var basic = requestBodyObject.get("basic");
				
					var responseTopic = "SeQLock/response/user" + userid + "/" + timestamp;
				
					System.out.println("Response Topic: " + responseTopic);
				
					basic = basic.toString().replaceAll("\\s+", "");
				
					for (User user: users) {
						if (user.getBasicAuth().equals(basic)) {
							this.publish(responseTopic, "1");
							return;
						}
					}
					this.publish(responseTopic, "2");
				} catch (Exception e) {
					System.out.println("Error in JSON request!");
				}
			}
		};
		client.subscribe("SeQLock/verify");
		System.out.println("Secure Server now listens to topic SeQLock/verify...");
	}
	
	public void addUser(String username, String password) {
		users.add(new User(username, password));
	}
	
	public static void main(String[] args) {
		var server = new SecureServer();
		server.addUser("jokab", "asd123");
		server.addUser("mett", "321dsa");
		server.startup();
	}
}
// mvn compiler:compile exec:java -Dexec.mainClass=com.SeQLock.SecureServer.SecureServer
