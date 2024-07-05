import { CallingState, StreamCall, StreamVideo, StreamVideoClient, useCallStateHooks, User, StreamTheme, StreamVideoParticipant, ParticipantView } from '@stream-io/video-react-sdk';

import '@stream-io/video-react-sdk/dist/css/styles.css';

// Remember to update the API key and token values because it changes every day.
const apiKey = 'bnvmc79qtrxy';
const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiRGFuaWVsLVRlc3RpbmctMSJ9.TZv1zfLXJ9xCdusRgBQBw23HSn3pW-w3piGfSm7YYNk';
const userId = 'Daniel-Testing-1';
const callId = 'Daniel-Testing-Room';

// set up the user object
const user: User = {
  id: userId,
  name: 'Daniel-Testing-1',
  image: 'https://getstream.io/random_svg/?id=oliver&name=Oliver',
};

const client = new StreamVideoClient({ apiKey, user, token });
const call = client.call('default', callId);
await call.join({ create: true });

export default function VideoCall () {
  return (
    <StreamVideo client={client}>
      <StreamCall call={call}>
        <MyUILayout />
      </StreamCall>
    </StreamVideo>
  );
}

export const MyParticipantList = (props: { participants: StreamVideoParticipant[] }) => {
  const { participants } = props;
  return (
    <div style={{ display: 'flex', flexDirection: 'row', gap: '8px' }}>
      {participants.map((participant) => (
        <ParticipantView participant={participant} key={participant.sessionId} />
      ))}
    </div>
  );
};

export const MyFloatingLocalParticipant = (props: { participant?: StreamVideoParticipant }) => {
  const { participant } = props;
  return (
    <div
      style={{
        position:"absolute",
        top:"15px",
        left:"15px",
        width:"240px",
        height:"135px",
        boxShadow:"rgba(0,0,0, 0.1) 0px 0px 10px 3px",
        borderRadius:"12px"
      }}
    >
      <ParticipantView participant={participant!} />
    </div>
  )
}

export const MyUILayout = () => {
  const { useCallCallingState, useLocalParticipant, useRemoteParticipants } = useCallStateHooks();

  const callingState = useCallCallingState();
  const localParticipant = useLocalParticipant();
  const remoteParticipants = useRemoteParticipants();

  if (callingState !== CallingState.JOINED) {
    return <div>Loading...</div>;
  }

  return (
    <StreamTheme>
      <MyParticipantList participants={remoteParticipants} />
      <MyFloatingLocalParticipant participant={localParticipant} />
    </StreamTheme>
  );
};
