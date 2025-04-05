import fs from "fs";
import csv from "csv-parser";
import { AI } from "@cot/sdk";
import async from "async";

interface FAQChannelData {
  "question": string;
  "answer": string;
  "mtnapp_answer": string;
  "question_hash": string;
  "answer_hash": string;
  "metadata": string;
}
const isEmpty = (s: any) => s == null || s === "";
const isNotEmpty = (s: any) => !isEmpty(s)
const processor = () => {
  const ai = new AI()
  if (fs.existsSync(__dirname + "/../faq_channels_out.csv")) {
    fs.unlinkSync(__dirname + "/../faq_channels_out.csv")
  }
  const headers: Array<keyof FAQChannelData> = ["question", "answer", "mtnapp_answer", "question_hash", "answer_hash", "metadata"]
  const input = fs.createReadStream(__dirname + "/../faq_channels.csv", {

  })
  const output = fs.createWriteStream(__dirname + "/../faq_channels_out.csv")
  output.write(headers.join(",") + "\n");
  const push_flush = (row: FAQChannelData) => {
    // Write the processed row to the output file
    output.write(headers.map((header) => {
      if (row[header].startsWith("\"") && row[header].endsWith("\"")) {
        return row[header]
      }
      else if (row[header].startsWith("\"")) {
        return `"${row[header].substring(1).replace(/[\"]/g, '\'') ?? ""}"`
      }
      else if (row[header].endsWith("\"")) {
        return `"${row[header].substring(0, row[header].length-1).replace(/[\"]/g, '\'') ?? ""}"`
      }
      else {
        return `"${row[header]?.replace(/[\"]/g, '\'') ?? ""}"`
      }
    }).join(",") + "\n");
  }


  // Create a queue with a concurrency limit (e.g., process 2 rows at a time)
  const queue = async.queue(async (row: FAQChannelData, callback) => {
    try {
      const question = row.question.toLowerCase()
      const metadata = row.metadata.toLowerCase()
      const answer = row.answer.toLowerCase()
      if (question.includes("mymtn app") || question.includes("my mtn app") || question.includes("mymtnapp") || question.includes("mymtn ng app")) {
        push_flush({ ...row, mtnapp_answer: isNotEmpty(row.mtnapp_answer) ? row.mtnapp_answer : row.answer })
      }
      else if (answer.includes("mymtnapp") || answer.includes("mymtn ng app") || answer.includes("mymtn ng app") || answer.includes("mymtn app") || answer.includes("mymtnng") || answer.includes("mymtn ng")) {
        const answer = row.answer.split("\n").find((answer) => answer.toLowerCase().includes("mymtnapp") || answer.toLowerCase().includes("mymtn app") || answer.toLowerCase().includes("mymtnng") || answer.toLowerCase().includes("mymtn ng app"))
        if (answer?.toLowerCase().includes("dial")) {
          push_flush({
            ...row,
          })
        } else {
          push_flush({
            ...row,
            mtnapp_answer: answer?.replace("\"", "'") ?? row.answer
          })
        }
      }
      else if (metadata.includes("myMTN NG App")) {
        push_flush({
          ...row,
          mtnapp_answer: isNotEmpty(row.mtnapp_answer) ? row.mtnapp_answer : row.answer
        })
      }
      else {
        push_flush(row)
      }
      // Notify the queue that this task is done

      callback();
    } catch (err) {
      console.error('Error processing row:', err);
      callback(err as Error); // Pass the error to the queue
    }
  }, 1); // Concurrency limit: 1

  // Handle queue completion
  queue.drain(() => {
    console.log('All rows have been processed.');
    // output.end(); // Close the output stream
  });

  // Handle queue errors
  queue.error((err) => {
    console.error('Queue error:', err);
    output.end(); // Close the output stream in case of error
  });
  let index = 0;
  input.pipe(csv())
    .on('data', (row: FAQChannelData) => {
      // Add each row to the queue for processing
      index++
      queue.push(row);
    })
    .on('end', () => {
      console.log('Finished reading the file.', index+1);
    })
    .on('error', (err) => {
      console.error('Error reading the file:', err);
    });
}

processor()