# sdx-sequence

Scalable service for generating sequences for SDX (backed by MongoDB)

## API

There are three endpoints for the three types of sequences:
 * `GET /sequence`
 * `GET /batch-sequence`
 * `GET /image-sequence`

# Query response

For any of the endpoints the response will look like:
```
{
    sequence_no: 1
}
```
