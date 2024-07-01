import 'firebase/compat/auth';
import 'firebase/compat/firestore';
import { initializeApp } from "firebase/app";
import {getAuth,GoogleAuthProvider} from "firebase/auth";
import {getFirestore} from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyByeQrLwVNoW_V2ElJ9R_w-ma7LBG8XETA",
  authDomain: "finance-53aba.firebaseapp.com",
  projectId: "finance-53aba",
  storageBucket: "finance-53aba.appspot.com",
  messagingSenderId: "627188669119",
  appId: "1:627188669119:web:eb3d1676b01034aee3440a",
  measurementId: "G-LBFTQ5QN1H"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth=getAuth(app);
export const db=getFirestore(app);
export{auth };
export const googleprovider=new GoogleAuthProvider();