# C# and .NET rules

Read [common rules](README.md). Identify the .NET SDK/runtime, target frameworks,
C# version, nullable/analyzer settings, ASP.NET and EF Core versions when used,
and supported deployment baseline.

- Enable nullable analysis for new code and address warnings honestly; avoid !
  merely to silence boundary nullability. Use records for suitable immutable
  contracts/value types and separate tracked entities from protocol DTOs.
- Use async/await end to end for IO. Propagate CancellationToken and observe
  Tasks; avoid .Result/.Wait(), unobserved fire-and-forget work, and async void
  outside event handlers. Do not wrap already asynchronous IO in Task.Run.
- Use explicit service lifetimes. Keep scoped dependencies out of singletons;
  background workers create/dispose their own scopes. Reuse configured HTTP
  clients and dispose owned resources with using/await using as appropriate.
- DbContext is not safe for parallel operations. Keep database transactions short,
  write operation/outbox records atomically, and send partner commands after
  commit. Configure query shape instead of relying on lazy entity serialization.
- Use decimal, explicit currency/rounding, DateTimeOffset/UTC, and explicit
  System.Text.Json mappings. Separate transport exceptions, cancellation, domain
  rejection, and OCPI response status.
- Run dotnet build/test and configured analyzers/format checks for the selected
  target. Test DI lifetimes, cancellation, JSON compatibility, transactions, and
  authorization where the change depends on runtime behavior.

## Security controls

Names are starting points: confirm them for the installed version.

- **Randomness, comparison, crypto:** RandomNumberGenerator;
  CryptographicOperations.FixedTimeEquals; AesGcm with a fresh nonce; ASP.NET Core Data
  Protection for app-managed secrets, with keys persisted and protected across instances.
- **Secret leaks:** a C# record's generated ToString prints every property. Override it
  on secret-bearing records and use log redaction for structured logging.
- **Outbound:** never return true from ServerCertificateCustomValidationCallback or use
  DangerousAcceptAnyServerCertificateValidator. Set AllowAutoRedirect to false on partner
  calls; use SocketsHttpHandler.ConnectCallback to check resolved addresses; limit
  MaxResponseContentBufferSize. Set timeouts through a CancellationToken.
- **WebSockets:** AcceptWebSocketAsync does not limit message size, so enforce a cap in
  your receive loop. Authenticate before accepting. Set MaxRequestBodySize in Kestrel.
- **Proxies:** in ForwardedHeaders options, list your known proxies and networks explicitly,
  and restrict ForwardLimit. Use certificate forwarding only behind a proxy you trust.
- **mTLS:** set Kestrel's ClientCertificateMode to require it on the station host, and use
  the certificate authentication handler with chain validation and an identity check.
- **Parsing and SQL:** no BinaryFormatter, and no Newtonsoft TypeNameHandling on untrusted
  input. Use EF Core parameters; if you use global query filters for tenancy, audit
  every IgnoreQueryFilters call and test the filter on each entity.
- **Authorization:** use policies on application services. Blazor UI checks are display
  only, and server code must check again.

Official sources: [C# async scenarios](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/async-scenarios),
[.NET dependency-injection guidelines](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-guidelines),
and [EF Core DbContext lifetime](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/).
Recheck the selected release's migration and support guidance at use time.
