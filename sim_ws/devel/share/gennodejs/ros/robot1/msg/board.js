// Auto-generated. Do not edit!

// (in-package robot1.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class board {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.table = null;
    }
    else {
      if (initObj.hasOwnProperty('table')) {
        this.table = initObj.table
      }
      else {
        this.table = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type board
    // Serialize message field [table]
    bufferOffset = _arraySerializer.uint32(obj.table, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type board
    let len;
    let data = new board(null);
    // Deserialize message field [table]
    data.table = _arrayDeserializer.uint32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 4 * object.table.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'robot1/board';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'f4fc566b67f0715ec037ec3bb197f924';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint32[] table
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new board(null);
    if (msg.table !== undefined) {
      resolved.table = msg.table;
    }
    else {
      resolved.table = []
    }

    return resolved;
    }
};

module.exports = board;
