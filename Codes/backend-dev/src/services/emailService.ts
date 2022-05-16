import sgMail from "@sendgrid/mail";
sgMail.setApiKey(process.env.SENDGRID_API_KEY || "");

const appName = process.env.APP_NAME;
const emailFrom = process.env.EMAIL_FROM || "no-reply@" + appName;
const frontEndUrL = process.env.FRONTEND_URL;

export const sendWelcomeEmail = async (token: string, to: string) => {
  const mail = {
    from: emailFrom,
    to: to,
    subject: `Welcome to ${appName}`,
    html: `Hello, <br/><br/>
    Please click below link to login your ${appName} account <br/>
    <a style="margin: 15px 3px;width: 250px;color:#ffffff;display:block;text-align:center;text-decoration:none;background: #b380b9;border-radius: 5px;line-height: 38px;"
    href="${frontEndUrL}/reset-password/?token=${token}&mail=${to}"> Sign in to ${appName} </a>
    <br/><br/> Thank you, <br/> ${appName} Team`,
  };
  await sgMail.send(mail);
};
export const sendPasswordResetEmail = async (token: string, to: string) => {
  const mail = {
    to: to,
    from: emailFrom,
    subject: `Reset your ${appName} password`,
    html: `Hello, <br/><br/>
    Please click below link to login your ${appName} account <br/>
    <a style="margin: 15px 3px;width: 250px;color:#ffffff;display:block;text-align:center;text-decoration:none;background: #ff8210;border-radius: 5px;line-height: 38px;"
    href="${frontEndUrL}/reset-password/?token=${token}&mail=${to}">Sign to ${appName}</a>
    <br/><br/> Thank you, <br/> ${appName} Team`,
  };
  await sgMail.send(mail);
};
