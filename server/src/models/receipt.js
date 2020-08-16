const mongoose = require('mongoose');

const { Schema } = mongoose;

const receiptSchema = new Schema(
// schema
  {
    Date: {
      type: Date,
      required: true,
    },
    Shop: {
      type: String,
      required: true,
    },
    Spent: {
      type: Number,
      required: true,
      min: 0,
    },
    Payer: {
      type: String,
      required: true,
    },
    Description: String,
  },
  // options
  {
    timestamps: true,
  },
);

const receipt = mongoose.model('Receipt', receiptSchema);

module.exports = receipt;
