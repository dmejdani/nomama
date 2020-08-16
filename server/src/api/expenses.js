const { Router } = require('express');

const router = Router();
const ReceiptEntry = require('../models/receipt');

router.get('/', (req, res) => {
  res.json({
    message: 'Just checking',
  });
});

router.post('/', async (req, res) => {
  try {
    const receiptEntry = new ReceiptEntry(req.body);
    const createdEntry = await receiptEntry.save();
    res.json(createdEntry);
    console.log(req.body);
  } catch (error) {
    
  }
});

module.exports = router;
