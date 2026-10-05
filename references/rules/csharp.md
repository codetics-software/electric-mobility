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

Official sources: [C# async scenarios](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/async-scenarios),
[.NET dependency-injection guidelines](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-guidelines),
and [EF Core DbContext lifetime](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/).
Recheck the selected release's migration and support guidance at use time.
