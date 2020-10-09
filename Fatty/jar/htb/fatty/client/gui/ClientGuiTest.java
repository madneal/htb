package htb.fatty.client.gui;

import htb.fatty.client.connection.Connection;
import htb.fatty.client.methods.Invoker;
import htb.fatty.shared.message.MessageBuildException;
import htb.fatty.shared.resources.User;
import java.awt.Color;
import java.awt.EventQueue;
import java.awt.Font;
import java.awt.LayoutManager;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.IOException;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JLayeredPane;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.JTextPane;
import javax.swing.border.EmptyBorder;

public class ClientGuiTest extends JFrame {
  private JPanel contentPane;
  
  private JTextField tfUsername;
  
  private JPasswordField tfPassword;
  
  private User user;
  
  private Connection conn;
  
  private Invoker invoker;
  
  private JTextField fileTextField;
  
  private JTextField textField_1;
  
  private JTextField textField_2;
  
  private String currentFolder = null;
  
  public static void main(String[] args) {
    EventQueue.invokeLater(new Runnable() {
          public void run() {
            try {
              ClientGuiTest frame = new ClientGuiTest();
              frame.setVisible(true);
            } catch (Exception e) {
              e.printStackTrace();
            } 
          }
        });
  }
  
  public ClientGuiTest() {
    setDefaultCloseOperation(3);
    setBounds(100, 100, 872, 691);
    JMenuBar menuBar = new JMenuBar();
    setJMenuBar(menuBar);
    JMenu fileMenu = new JMenu("File");
    menuBar.add(fileMenu);
    JMenuItem exit = new JMenuItem("Exit");
    fileMenu.add(exit);
    exit.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            if (ClientGuiTest.this.conn != null) {
              ClientGuiTest.this.conn.logoff();
              ClientGuiTest.this.conn.close();
            } 
            ClientGuiTest.this.dispose();
            System.exit(0);
          }
        });
    JMenu profileMenu = new JMenu("Profile");
    menuBar.add(profileMenu);
    final JMenuItem whoami = new JMenuItem("Whoami");
    whoami.setEnabled(true);
    profileMenu.add(whoami);
    final JMenuItem changePassword = new JMenuItem("ChangePassword");
    changePassword.setEnabled(true);
    profileMenu.add(changePassword);
    JMenu statusMenu = new JMenu("ServerStatus");
    menuBar.add(statusMenu);
    final JMenuItem uname = new JMenuItem("Uname");
    uname.setEnabled(true);
    statusMenu.add(uname);
    final JMenuItem users = new JMenuItem("Users");
    users.setEnabled(true);
    statusMenu.add(users);
    final JMenuItem netstat = new JMenuItem("Nestat");
    netstat.setEnabled(true);
    statusMenu.add(netstat);
    final JMenuItem ipconfig = new JMenuItem("Ipconfig");
    ipconfig.setEnabled(true);
    statusMenu.add(ipconfig);
    JMenu fileBrowser = new JMenu("FileBrowser");
    menuBar.add(fileBrowser);
    final JMenuItem configs = new JMenuItem("Configs");
    configs.setEnabled(true);
    fileBrowser.add(configs);
    final JMenuItem notes = new JMenuItem("Notes");
    notes.setEnabled(true);
    fileBrowser.add(notes);
    final JMenuItem mail = new JMenuItem("Mail");
    mail.setEnabled(true);
    fileBrowser.add(mail);
    JMenu connectionTest = new JMenu("ConnectionTest");
    menuBar.add(connectionTest);
    final JMenuItem ping = new JMenuItem("Ping");
    ping.setEnabled(true);
    connectionTest.add(ping);
    JMenu help = new JMenu("Help");
    menuBar.add(help);
    JMenuItem contact = new JMenuItem("Contact");
    help.add(contact);
    JMenuItem about = new JMenuItem("About");
    help.add(about);
    this.contentPane = new JPanel();
    this.contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
    setContentPane(this.contentPane);
    this.contentPane.setLayout((LayoutManager)null);
    JLayeredPane layeredPane = new JLayeredPane();
    layeredPane.setBounds(222, 193, 1, 1);
    this.contentPane.add(layeredPane);
    final JPanel controlPanel = new JPanel();
    controlPanel.setBounds(0, 0, 872, 638);
    controlPanel.setVisible(false);
    this.contentPane.add(controlPanel);
    controlPanel.setLayout((LayoutManager)null);
    JPanel panel = new JPanel();
    panel.setBackground(Color.WHITE);
    panel.setBounds(12, 12, 848, 583);
    controlPanel.add(panel);
    panel.setLayout((LayoutManager)null);
    final JTextPane textPane = new JTextPane();
    textPane.setEditable(false);
    textPane.setBounds(12, 12, 824, 559);
    panel.add(textPane);
    this.fileTextField = new JTextField();
    this.fileTextField.setBounds(28, 607, 164, 25);
    controlPanel.add(this.fileTextField);
    this.fileTextField.setColumns(10);
    JButton openFileButton = new JButton("Open");
    openFileButton.setBounds(204, 607, 114, 25);
    controlPanel.add(openFileButton);
    JButton btnClear = new JButton("Clear");
    btnClear.setBounds(731, 607, 114, 25);
    controlPanel.add(btnClear);
    final JPanel LoginPanel = new JPanel();
    LoginPanel.setBounds(12, 12, 944, 844);
    this.contentPane.add(LoginPanel);
    LoginPanel.setLayout((LayoutManager)null);
    JLabel lblNewLabel = new JLabel("Username:");
    lblNewLabel.setFont(new Font("Dialog", 1, 14));
    lblNewLabel.setBounds(118, 197, 151, 68);
    LoginPanel.add(lblNewLabel);
    this.tfUsername = new JTextField();
    this.tfUsername.setBounds(294, 218, 396, 27);
    LoginPanel.add(this.tfUsername);
    this.tfUsername.setColumns(10);
    this.tfPassword = new JPasswordField();
    this.tfPassword.setColumns(10);
    this.tfPassword.setBounds(294, 280, 396, 27);
    LoginPanel.add(this.tfPassword);
    JButton btnNewButton = new JButton("Login ");
    btnNewButton.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String username = ClientGuiTest.this.tfUsername.getText().trim();
            String password = new String(ClientGuiTest.this.tfPassword.getPassword());
            ClientGuiTest.this.user = new User();
            ClientGuiTest.this.user.setUsername(username);
            ClientGuiTest.this.user.setPassword(password);
            try {
              ClientGuiTest.this.conn = Connection.getConnection();
            } catch (htb.fatty.client.connection.Connection.ConnectionException e1) {
              JOptionPane.showMessageDialog(LoginPanel, "Connection Error!", "Error", 0);
              return;
            } 
            if (ClientGuiTest.this.conn.login(ClientGuiTest.this.user)) {
              JOptionPane.showMessageDialog(LoginPanel, "Login Successful!", "Login", 1);
              LoginPanel.setVisible(false);
              String roleName = ClientGuiTest.this.conn.getRoleName();
              ClientGuiTest.this.user.setRoleByName(roleName);
              if (roleName.contentEquals("admin")) {
                uname.setEnabled(true);
                users.setEnabled(true);
                netstat.setEnabled(true);
                ipconfig.setEnabled(true);
                changePassword.setEnabled(true);
              } 
              if (!roleName.contentEquals("anonymous")) {
                whoami.setEnabled(true);
                configs.setEnabled(true);
                notes.setEnabled(true);
                mail.setEnabled(true);
                ping.setEnabled(true);
              } 
              ClientGuiTest.this.invoker = new Invoker(ClientGuiTest.this.conn, ClientGuiTest.this.user);
              controlPanel.setVisible(true);
            } else {
              JOptionPane.showMessageDialog(LoginPanel, "Login Failed!", "Login", 1);
              ClientGuiTest.this.conn.close();
            } 
          }
        });
    btnNewButton.setBounds(572, 339, 117, 25);
    LoginPanel.add(btnNewButton);
    JLabel lblPassword = new JLabel("Password:");
    lblPassword.setFont(new Font("Dialog", 1, 14));
    lblPassword.setBounds(118, 259, 151, 68);
    LoginPanel.add(lblPassword);
    final JPanel passwordChange = new JPanel();
    passwordChange.setBounds(0, 0, 860, 638);
    passwordChange.setVisible(false);
    this.contentPane.add(passwordChange);
    passwordChange.setLayout((LayoutManager)null);
    this.textField_1 = new JTextField();
    this.textField_1.setBounds(355, 258, 263, 29);
    passwordChange.add(this.textField_1);
    this.textField_1.setColumns(10);
    JLabel lblOldPassword = new JLabel("Old Password:");
    lblOldPassword.setFont(new Font("Dialog", 1, 14));
    lblOldPassword.setBounds(206, 265, 131, 17);
    passwordChange.add(lblOldPassword);
    JLabel lblNewPassword = new JLabel("New Password:");
    lblNewPassword.setFont(new Font("Dialog", 1, 14));
    lblNewPassword.setBounds(206, 322, 131, 15);
    passwordChange.add(lblNewPassword);
    this.textField_2 = new JTextField();
    this.textField_2.setBounds(355, 308, 263, 29);
    passwordChange.add(this.textField_2);
    this.textField_2.setColumns(10);
    JButton pwChangeButton = new JButton("Change");
    pwChangeButton.setBounds(575, 349, 114, 25);
    passwordChange.add(pwChangeButton);
    about.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String response = ClientGuiTest.this.invoker.about();
            textPane.setText(response);
          }
        });
    contact.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String response = ClientGuiTest.this.invoker.contact();
            textPane.setText(response);
          }
        });
    btnClear.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            textPane.setText("");
          }
        });
    ping.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String response = "";
            try {
              response = ClientGuiTest.this.invoker.ping();
            } catch (MessageBuildException|htb.fatty.shared.message.MessageParseException e1) {
              JOptionPane.showMessageDialog(controlPanel, "Failure during message building/parsing.", "Error", 0);
            } catch (IOException e2) {
              JOptionPane.showMessageDialog(controlPanel, "Unable to contact the server. If this problem remains, please close and reopen the client.", "Error", 0);
            } 
            textPane.setText(response);
          }
        });
    whoami.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String response = "";
            try {
              response = ClientGuiTest.this.invoker.whoami();
            } catch (MessageBuildException|htb.fatty.shared.message.MessageParseException e1) {
              JOptionPane.showMessageDialog(controlPanel, "Failure during message building/parsing.", "Error", 0);
            } catch (IOException e2) {
              JOptionPane.showMessageDialog(controlPanel, "Unable to contact the server. If this problem remains, please close and reopen the client.", "Error", 0);
            } 
            textPane.setText(response);
          }
        });
    configs.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String response = "";
            ClientGuiTest.this.currentFolder = "configs";
            try {
              response = ClientGuiTest.this.invoker.showFiles("configs");
            } catch (MessageBuildException|htb.fatty.shared.message.MessageParseException e1) {
              JOptionPane.showMessageDialog(controlPanel, "Failure during message building/parsing.", "Error", 0);
            } catch (IOException e2) {
              JOptionPane.showMessageDialog(controlPanel, "Unable to contact the server. If this problem remains, please close and reopen the client.", "Error", 0);
            } 
            textPane.setText(response);
          }
        });
    notes.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String response = "";
            ClientGuiTest.this.currentFolder = "notes";
            try {
              response = ClientGuiTest.this.invoker.showFiles("notes");
            } catch (MessageBuildException|htb.fatty.shared.message.MessageParseException e1) {
              JOptionPane.showMessageDialog(controlPanel, "Failure during message building/parsing.", "Error", 0);
            } catch (IOException e2) {
              JOptionPane.showMessageDialog(controlPanel, "Unable to contact the server. If this problem remains, please close and reopen the client.", "Error", 0);
            } 
            textPane.setText(response);
          }
        });
    mail.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String response = "";
            ClientGuiTest.this.currentFolder = "mail";
            try {
              response = ClientGuiTest.this.invoker.showFiles("mail");
            } catch (MessageBuildException|htb.fatty.shared.message.MessageParseException e1) {
              JOptionPane.showMessageDialog(controlPanel, "Failure during message building/parsing.", "Error", 0);
            } catch (IOException e2) {
              JOptionPane.showMessageDialog(controlPanel, "Unable to contact the server. If this problem remains, please close and reopen the client.", "Error", 0);
            } 
            textPane.setText(response);
          }
        });
    openFileButton.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            if (ClientGuiTest.this.currentFolder == null) {
              JOptionPane.showMessageDialog(controlPanel, "No folder selected! List a directory first!", "Error", 0);
              return;
            } 
            String response = "";
            String fileName = ClientGuiTest.this.fileTextField.getText();
            fileName.replaceAll("[^a-zA-Z0-9.]", "");
            try {
              response = ClientGuiTest.this.invoker.open(ClientGuiTest.this.currentFolder, fileName);
            } catch (MessageBuildException|htb.fatty.shared.message.MessageParseException e1) {
              JOptionPane.showMessageDialog(controlPanel, "Failure during message building/parsing.", "Error", 0);
            } catch (IOException e2) {
              JOptionPane.showMessageDialog(controlPanel, "Unable to contact the server. If this problem remains, please close and reopen the client.", "Error", 0);
            } 
            textPane.setText(response);
          }
        });
    uname.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String response = "";
            try {
              response = ClientGuiTest.this.invoker.uname();
            } catch (MessageBuildException|htb.fatty.shared.message.MessageParseException e1) {
              JOptionPane.showMessageDialog(controlPanel, "Failure during message building/parsing.", "Error", 0);
            } catch (IOException e2) {
              JOptionPane.showMessageDialog(controlPanel, "Unable to contact the server. If this problem remains, please close and reopen the client.", "Error", 0);
            } 
            textPane.setText(response);
          }
        });
    users.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String response = "";
            try {
              response = ClientGuiTest.this.invoker.users();
            } catch (MessageBuildException|htb.fatty.shared.message.MessageParseException e1) {
              JOptionPane.showMessageDialog(controlPanel, "Failure during message building/parsing.", "Error", 0);
            } catch (IOException e2) {
              JOptionPane.showMessageDialog(controlPanel, "Unable to contact the server. If this problem remains, please close and reopen the client.", "Error", 0);
            } 
            textPane.setText(response);
          }
        });
    ipconfig.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String response = "";
            try {
              response = ClientGuiTest.this.invoker.ipconfig();
            } catch (MessageBuildException|htb.fatty.shared.message.MessageParseException e1) {
              JOptionPane.showMessageDialog(controlPanel, "Failure during message building/parsing.", "Error", 0);
            } catch (IOException e2) {
              JOptionPane.showMessageDialog(controlPanel, "Unable to contact the server. If this problem remains, please close and reopen the client.", "Error", 0);
            } 
            textPane.setText(response);
          }
        });
    netstat.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String response = "";
            try {
              response = ClientGuiTest.this.invoker.netstat();
            } catch (MessageBuildException|htb.fatty.shared.message.MessageParseException e1) {
              JOptionPane.showMessageDialog(controlPanel, "Failure during message building/parsing.", "Error", 0);
            } catch (IOException e2) {
              JOptionPane.showMessageDialog(controlPanel, "Unable to contact the server. If this problem remains, please close and reopen the client.", "Error", 0);
            } 
            textPane.setText(response);
          }
        });
    changePassword.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            controlPanel.setVisible(false);
            passwordChange.setVisible(true);
          }
        });
    pwChangeButton.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            JOptionPane.showMessageDialog(passwordChange, "Not implemented yet.", "Error", 0);
            passwordChange.setVisible(false);
            controlPanel.setVisible(true);
          }
        });
    addWindowListener(new WindowAdapter() {
          public void windowClosing(WindowEvent e) {
            System.out.println("Closed");
            if (ClientGuiTest.this.conn != null) {
              ClientGuiTest.this.conn.logoff();
              ClientGuiTest.this.conn.close();
            } 
            e.getWindow().dispose();
            System.exit(0);
          }
        });
  }
}

