package com.SeQLock.SecureServer.model;

import java.util.Base64;

public class User {
	private final String username;
	private final String password;
	
	public User(String username, String password) {
		this.password = password;
		this.username = username;
	}
	
	public String getUsername() {
		return this.username;
	}
	
	public String getBasicAuth() {
		return Base64.getEncoder().encodeToString((username + ":" + password).getBytes());
	}

}
