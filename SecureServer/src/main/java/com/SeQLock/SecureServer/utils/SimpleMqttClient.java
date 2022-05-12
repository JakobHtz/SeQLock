package com.SeQLock.SecureServer.utils;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class SimpleMqttClient implements MqttCallback {
	private String host = "localhost";
	private int port = 1883;
	private String clientID = "SecureServer";
	private String password = "test";
	private MqttClient client;
	private MemoryPersistence persistence = new MemoryPersistence();

	public SimpleMqttClient(String host, int port, String clientID) {
		super();
		this.host = host;
		this.port = port;
		this.clientID = clientID;
		openConnection();
	}
	
	public SimpleMqttClient(String host, int port) {
		super();
		this.host = host;
		this.port = port;
		openConnection();
	}
	
	public SimpleMqttClient(String host) {
		super();
		this.host = host;
		openConnection();
	}

	public SimpleMqttClient() {
		super();
		openConnection();
	}
	
	private void openConnection() {
		var broker = "tcp://" + host + ":" + port;
		System.out.println("Connecting to " + broker + " ...");
		try {
			client = new MqttClient(broker, clientID, persistence);
			var connOpts = new MqttConnectOptions();
			connOpts.setCleanSession(true);
		    connOpts.setUserName(clientID);
		    connOpts.setPassword(password.toCharArray());
			client.connect(connOpts);
			client.setCallback(this);
		} catch (MqttException e) {
			e.printStackTrace();
			System.exit(1);
		}
	}
	
	public void publish(String topic, String content) {
		try {
			var message = new MqttMessage(content.getBytes());
			System.out.println("message " + message);
			client.publish(topic, message);
		}
		catch (MqttException e) {
			System.out.println(e.getMessage());
			e.printStackTrace();
		}
		catch (Exception e) {
			System.out.println(e.getMessage());
			e.printStackTrace();
			System.exit(1);
		}
	}

	public void subscribe(String topic) {
		try {
			client.subscribe(topic);
		}
		catch (MqttException e) {
			System.out.println(e.getMessage());
			e.printStackTrace();
		}
		catch (Exception e) {
			System.out.println(e.getMessage());
			e.printStackTrace();
			System.exit(1);
		}
	}
	
	@Override
	public void messageArrived(String topic, MqttMessage message) throws Exception {
		System.out.println("message is : "+message);
	}

	@Override
	public void connectionLost(Throwable cause) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {
		// TODO Auto-generated method stub
		
	}
}
