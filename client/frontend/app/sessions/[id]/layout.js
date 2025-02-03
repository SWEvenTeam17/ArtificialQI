'use client'
import { ResponseProvider } from './../../components/contexts/ResponseContext';

export default function SessionLayout({children})
{
    return (
        <ResponseProvider children={children}/>
    )
}
