// import { S3Client, DeleteObjectsCommand } from '@aws-sdk/client-s3'
// import { s3Config } from '../controllers/uploadController'

// const s3Client = new S3Client(s3Config.s3Options)
// const bucket = process.env.S3_BUCKET
// const path = process.env.S3_PATH

export const deleteS3Objects = async (key: string) => {
  // const finalKey = `${path}/${key}`
  // const command = new DeleteObjectsCommand({
  //   Bucket: bucket,
  //   Delete: {
  //     Objects: [{ Key: finalKey }]
  //   }
  // })
  // await s3Client.send(command)
};
