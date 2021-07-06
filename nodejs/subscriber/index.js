/**
 * @fileoverview Description of this file.
 */
// set express
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const PORT = '8092' || process.env.PORT;
app.use(bodyParser.json());


//set pubsub 
const subscriptionName = 'demo-pubsub-sub';
const timeout = 600;

const {PubSub} = require('@google-cloud/pubsub');
const pubSubClient = new PubSub();

//set publish function
function listenForMessages() {
  const subscription = pubSubClient.subscription(subscriptionName);

  let messageCount =0;
  const messageHandler = message => {
    console.log(`Recieved message ${message.id}:`);
    console.log(`\tData" ${message.data}`);
    console.log(`\tAttributes: ${JSON.stringify(message.attributes)}`);
    messageCount += 1;

    //ack
    message.ack();
  };

  //listen new messages
  subscription.on('message', messageHandler);

  setTimeout(() => {
    subscription.removeListener('message', messageHandler);
    console.log(`${messageCount} message(s) recieved.`);
  }, timeout * 1000);
};

app.get('/', (req,res) => {
  res.send("frontend is ok");
});

app.get('/get', (req,res) => {
  listenForMessages();
});

app.listen(PORT, ()=> {
  console.log('running at port:' + PORT);
});
