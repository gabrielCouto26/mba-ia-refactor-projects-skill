const config = {
    port: process.env.PORT || 3000,
    dbUser: process.env.DB_USER,
    dbPass: process.env.DB_PASS,
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
    smtpUser: process.env.SMTP_USER,
    env: process.env.NODE_ENV || "development"
};

if (config.env === "production") {
    for (const name of ["dbUser", "dbPass", "paymentGatewayKey", "smtpUser"]) {
        if (!config[name]) {
            throw new Error(`Missing required production secret: ${name}`);
        }
    }
}

module.exports = config;
