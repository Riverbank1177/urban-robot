// Example using Node.js for broker API
const broker = require('broker-api');
async function executeOrder(direction, volume) {
    try {
        const order = await broker.createOrder({
            symbol: 'XAUUSD',
            type: direction,
            volume: volume
        });
    } catch(error) {
        console.log(error);
    }
}