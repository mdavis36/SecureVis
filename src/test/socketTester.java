package test;

import java.io.IOException;
import java.net.UnknownHostException;

import application.Communication;

public class socketTester {

	
	public static void main(String[] args) throws UnknownHostException, IOException, ClassNotFoundException {
		for (int i = 0; i < 5; i++ )  {
			Communication x = new Communication("hi");
			System.out.println(x.getReturnMessage());
		}
	}
	
}
