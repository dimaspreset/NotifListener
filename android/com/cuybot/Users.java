package com.cuybot;

public class Users {

    private String sender;
    private String message;
    private String notificationCode;

    // Default constructor required for Firebase
    public Users() {
    }

    public Users(String sender, String message, String notificationCode) {
        this.sender = sender != null ? sender : "";
        this.message = message != null ? message : "";
        this.notificationCode = notificationCode != null ? notificationCode : "";
    }

    // Getter methods
    public String getSender() {
        return sender;
    }

    public String getMessage() {
        return message;
    }

    public String getNotificationCode() {
        return notificationCode;
    }

    // Setter methods (required by Firebase)
    public void setSender(String sender) {
        this.sender = sender;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public void setNotificationCode(String notificationCode) {
        this.notificationCode = notificationCode;
    }

    @Override
    public String toString() {
        return "Users{" +
                "sender='" + sender + '\'' +
                ", message='" + message + '\'' +
                ", notificationCode='" + notificationCode + '\'' +
                '}';
    }
}