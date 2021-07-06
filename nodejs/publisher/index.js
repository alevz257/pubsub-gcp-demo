/**
 * @fileoverview Description of this file.
 */
// set express
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const PORT = '8091' || process.env.PORT;
app.use(bodyParser.json());


//set pubsub 
const topicName = 'demo-pubsub';
const data = JSON.stringify({foo: 'bar'});

const {PubSub} = require('@google-cloud/pubsub');
const pubSubClient = new PubSub();

//set publish function
async function publishMessage(message) {
  const dataBuffer = Buffer.from(message);
  
  const custAtt = {
    origin: 'frontend',
    test: 'test',
  };

  try {
    const messageId = await pubSubClient.topic(topicName).publish(dataBuffer,custAtt);
    console.log(`Message ${messageId} published.`);
  } catch (error) {
    console.error(`Recieved error while publishing: ${error.message}`);
    process.exitCode = 1;
  }
}

app.get('/', (req,res) => {
  res.send("frontend is ok");
});

app.post('/publish', (req,res) => {
  let messageBody = JSON.stringify(req.body.message);
  console.log(messageBody);
  publishMessage(messageBody);
  res.send(`Message ${messageBody} published.`);
});

app.listen(PORT, ()=> {
  console.log('running at port:' + PORT);
});
