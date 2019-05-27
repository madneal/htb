package com.myfirstplugin;

public class BlockyCore {
  public String sqlHost = "localhost";
  public String sqlUser = "root";
  public String sqlPass = "8YsqfCTnvxAUeduzjNSXe22";
  

  public BlockyCore() {}
  

  public void onServerStart() {}
  
  public void onServerStop() {}
  
  public void onPlayerJoin()
  {
    sendMessage("TODO get username", "Welcome to the BlockyCraft!!!!!!!");
  }
  
  public void sendMessage(String username, String message) {}
}
